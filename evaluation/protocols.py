"""Split protocols and metrics for the tractor evaluation.

The tractor clips are short segments cut from longer recordings, so segments of the
same recording are near-duplicates. A plain random split puts siblings on both sides of
the train/test boundary and inflates every metric. These helpers build recording-level
groups and splits that keep each group on one side only.

No audio or TensorFlow imports here, so this module is cheap to test.
"""
from __future__ import annotations

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (accuracy_score, average_precision_score, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler


def cluster_groups(features: np.ndarray, labels: np.ndarray, n_clusters_per_class: int) -> np.ndarray:
    """Assign pseudo-recording ids by clustering clips within each class.

    Clips that sound alike (same engine, same microphone, same session) land in one
    cluster, so keeping clusters intact on one side of a split removes sibling leakage.
    Clustering is done per class because one recording carries one label.
    """
    features = StandardScaler().fit_transform(features)
    groups = np.zeros(len(labels), dtype=int)
    offset = 0
    for cls in np.unique(labels):
        idx = np.where(labels == cls)[0]
        k = min(n_clusters_per_class, len(idx))
        ids = AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(features[idx])
        groups[idx] = ids + offset
        offset += k
    return groups


def random_splits(y: np.ndarray, n_splits: int, seed: int):
    """Stratified K-fold ignoring recordings (the leaky protocol)."""
    yield from StratifiedKFold(n_splits, shuffle=True, random_state=seed).split(np.zeros(len(y)), y)


def group_splits(y: np.ndarray, groups: np.ndarray, n_splits: int, seed: int):
    """Stratified K-fold where every group stays on one side (the honest protocol)."""
    for train, test in StratifiedGroupKFold(n_splits, shuffle=True, random_state=seed).split(
            np.zeros(len(y)), y, groups):
        assert not set(groups[train]) & set(groups[test]), "group leaked across the split"
        yield train, test


def metrics(y_true: np.ndarray, proba: np.ndarray, threshold: float = 0.5) -> dict:
    pred = (proba >= threshold).astype(int)
    out = {
        "accuracy": accuracy_score(y_true, pred),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred, zero_division=0),
        "f1": f1_score(y_true, pred, zero_division=0),
    }
    if len(np.unique(y_true)) == 2:
        out["roc_auc"] = roc_auc_score(y_true, proba)
        out["pr_auc"] = average_precision_score(y_true, proba)
    return out


def summarize(per_fold: list[dict]) -> dict:
    """Mean and standard deviation of each metric across folds."""
    keys = sorted({k for m in per_fold for k in m})
    return {k: (float(np.mean([m[k] for m in per_fold if k in m])),
                float(np.std([m[k] for m in per_fold if k in m]))) for k in keys}


def bootstrap_ci(y_true, proba, metric=f1_score, n=1000, seed=0, threshold=0.5):
    """95% bootstrap confidence interval of a metric over pooled out-of-fold predictions."""
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    pred = (np.asarray(proba) >= threshold).astype(int)
    scores = []
    for _ in range(n):
        i = rng.integers(0, len(y_true), len(y_true))
        if len(np.unique(y_true[i])) < 2:
            continue
        scores.append(metric(y_true[i], pred[i], zero_division=0))
    return float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))
