import numpy as np
import pytest

from protocols import bootstrap_ci, cluster_groups, group_splits, metrics, random_splits, summarize


def synthetic(n_sources=12, per_source=10, seed=0):
    """Each 'recording' has its own fingerprint; its segments are tiny perturbations of it."""
    rng = np.random.default_rng(seed)
    X, y, src = [], [], []
    for s in range(n_sources):
        center = rng.normal(0, 5, 8)
        for _ in range(per_source):
            X.append(center + rng.normal(0, 0.05, 8))
            y.append(s % 2)
            src.append(s)
    return np.array(X), np.array(y), np.array(src)


def test_group_splits_never_share_a_group():
    X, y, src = synthetic()
    for seed in range(3):
        for train, test in group_splits(y, src, 4, seed):
            assert not set(src[train]) & set(src[test])


def test_random_splits_do_leak_sources():
    """Documents why the random protocol is unsafe on segmented recordings."""
    X, y, src = synthetic()
    leaked = [bool(set(src[tr]) & set(src[te])) for tr, te in random_splits(y, 4, 0)]
    assert all(leaked)


def test_cluster_groups_recovers_sources_per_class():
    X, y, src = synthetic()
    groups = cluster_groups(X, y, n_clusters_per_class=6)
    for s in np.unique(src):
        assert len(set(groups[src == s])) == 1      # a recording is never split
    assert len(set(groups[y == 0]) & set(groups[y == 1])) == 0   # ids do not collide across classes


def test_group_split_removes_the_leak_effect():
    """A 1-NN classifier looks perfect when siblings leak, and falls to chance across sources."""
    from sklearn.neighbors import KNeighborsClassifier
    rng = np.random.default_rng(1)
    n_src, per = 16, 8
    centers = rng.normal(0, 5, (n_src, 8))
    src = np.repeat(np.arange(n_src), per)
    y = rng.integers(0, 2, n_src).repeat(per)          # labels unrelated to the sound
    X = centers[src] + rng.normal(0, 0.05, (len(src), 8))

    def acc(splits):
        out = []
        for tr, te in splits:
            out.append((KNeighborsClassifier(1).fit(X[tr], y[tr]).predict(X[te]) == y[te]).mean())
        return np.mean(out)

    assert acc(random_splits(y, 4, 0)) > 0.95
    assert acc(group_splits(y, src, 4, 0)) < 0.8


def test_metrics_and_summary():
    m = metrics(np.array([0, 0, 1, 1]), np.array([0.1, 0.4, 0.6, 0.9]))
    assert m["accuracy"] == 1.0 and m["roc_auc"] == 1.0
    s = summarize([{"f1": 0.5}, {"f1": 1.0}])
    assert s["f1"][0] == pytest.approx(0.75)


def test_bootstrap_ci_brackets_the_point_estimate():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 200)
    proba = np.clip(y * 0.6 + rng.normal(0.2, 0.2, 200), 0, 1)
    lo, hi = bootstrap_ci(y, proba)
    assert lo < hi
