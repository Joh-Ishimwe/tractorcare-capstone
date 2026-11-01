"""Leakage-aware evaluation of tractor sound classifiers.

    python run_evaluation.py                      # SVM + KNN, fast
    python run_evaluation.py --deep               # + simple CNN and ResNet-like CNN from scratch
    python run_evaluation.py --deep --pretrained path/to/resnet_like_cnn.h5   # + MIMII transfer

Experiments
  1. leakage:     every model under a random split vs a recording-grouped split
  2. granularity: SVM accuracy as the group definition gets finer (how fast does the leak vanish?)
  3. own-phone:   train on everything else, test on the phone recordings ("New Recording *")
Outputs go to evaluation/results/.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from protocols import bootstrap_ci, cluster_groups, group_splits, metrics, random_splits, summarize

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data" / "tractor"


def cross_validate(make_model, X, y, splits):
    per_fold, oof = [], np.full(len(y), np.nan)
    for train, test in splits:
        model = make_model().fit(X[train], y[train])
        proba = model.predict_proba(X[test])
        proba = proba[:, 1] if proba.ndim == 2 else proba
        oof[test] = proba
        per_fold.append(metrics(y[test], proba))
    return summarize(per_fold), oof


def fmt(s, k):
    return f"{s[k][0]:.3f} ± {s[k][1]:.3f}" if k in s else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deep", action="store_true")
    ap.add_argument("--pretrained", type=Path)
    ap.add_argument("--clusters", type=int, default=20, help="pseudo-recordings per class")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--epochs", type=int, default=25)
    a = ap.parse_args()

    from features import load_dataset
    import models

    M, S, y, names = load_dataset(DATA, ROOT / "cache" / "features.npz")
    print(f"{len(y)} clips: {int((y == 0).sum())} normal, {int((y == 1).sum())} abnormal")

    # Phone recordings are held out for experiment 3 and excluded from the CV experiments.
    phone = np.array([n.startswith("New Recording") for n in names])
    Mc, Sc, yc = M[~phone], S[~phone], y[~phone]
    groups = cluster_groups(Sc, yc, a.clusters)
    print(f"CV set: {len(yc)} clips in {len(set(groups))} pseudo-recording groups")

    registry = {"SVM (RBF)": (models.svm, Sc), "KNN (k=5)": (models.knn, Sc)}
    if a.deep:
        registry["Simple CNN"] = (lambda: models.KerasClassifier(models.simple_cnn, a.epochs), Mc)
        registry["ResNet-like CNN (scratch)"] = (lambda: models.KerasClassifier(models.resnet_cnn, a.epochs), Mc)
        if a.pretrained:
            registry["ResNet-like CNN (MIMII transfer)"] = (
                lambda: models.KerasClassifier(models.transfer_from(a.pretrained), a.epochs), Mc)

    results = {"n_clips": int(len(y)), "n_groups": int(len(set(groups))), "leakage": {}, "granularity": {}}

    # 1. leakage ---------------------------------------------------------------------------
    for name, (make, X) in registry.items():
        reps = 1 if "CNN" in name else a.repeats
        row = {}
        for proto in ("random", "grouped"):
            folds, oofs = [], []
            for r in range(reps):
                splits = (random_splits(yc, a.folds, r) if proto == "random"
                          else group_splits(yc, groups, a.folds, r))
                s, oof = cross_validate(make, X, yc, splits)
                folds.append(s)
                oofs.append(oof)
            avg = {k: (float(np.mean([f[k][0] for f in folds])), float(np.mean([f[k][1] for f in folds])))
                   for k in folds[0]}
            ci = bootstrap_ci(yc, np.nanmean(oofs, axis=0), threshold=0.5)
            row[proto] = {"summary": avg, "f1_ci95": ci}
        results["leakage"][name] = row
        print(f"{name:34s} random acc {fmt(row['random']['summary'], 'accuracy')} | "
              f"grouped acc {fmt(row['grouped']['summary'], 'accuracy')}  "
              f"F1 {fmt(row['grouped']['summary'], 'f1')}  AUC {fmt(row['grouped']['summary'], 'roc_auc')}")

    # 2. granularity -----------------------------------------------------------------------
    for k in (5, 10, 20, 40, 70):
        g = cluster_groups(Sc, yc, k)
        s, _ = cross_validate(models.svm, Sc, yc, group_splits(yc, g, a.folds, 0))
        results["granularity"][k] = s
        print(f"groups/class={k:3d}  SVM grouped acc {fmt(s, 'accuracy')}")

    # 3. own phone recordings --------------------------------------------------------------
    if phone.any():
        model = models.svm().fit(Sc, yc)
        proba = model.predict_proba(S[phone])[:, 1]
        results["phone"] = {"n": int(phone.sum()), "recall": float((proba >= 0.5).mean()),
                            "mean_p_abnormal": float(proba.mean())}
        print(f"phone recordings ({phone.sum()} abnormal): SVM recall {results['phone']['recall']:.2f}")

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, indent=2, default=float))
    write_report(results, out / "RESULTS.md")
    try:
        plot(results, out)
    except Exception as e:
        print("plot skipped:", e)


def write_report(r, path):
    L = ["# Tractor sound classification: leakage-aware results", "",
         f"{r['n_clips']} clips; cross-validation uses {r['n_groups']} pseudo-recording groups.", "",
         "| Model | Acc (random split) | Acc (grouped) | F1 (grouped) | ROC-AUC (grouped) | F1 95% CI |",
         "|---|---|---|---|---|---|"]
    for n, row in r["leakage"].items():
        g = row["grouped"]
        L.append(f"| {n} | {fmt(row['random']['summary'], 'accuracy')} | {fmt(g['summary'], 'accuracy')} | "
                 f"{fmt(g['summary'], 'f1')} | {fmt(g['summary'], 'roc_auc')} | "
                 f"[{g['f1_ci95'][0]:.2f}, {g['f1_ci95'][1]:.2f}] |")
    L += ["", "## Accuracy vs group granularity (SVM)", "", "| groups/class | accuracy |", "|---|---|"]
    L += [f"| {k} | {fmt(s, 'accuracy')} |" for k, s in r["granularity"].items()]
    if "phone" in r:
        p = r["phone"]
        L += ["", f"## Own phone recordings ({p['n']} abnormal clips, never used in training)", "",
              f"SVM recall: {p['recall']:.2f}; mean P(abnormal): {p['mean_p_abnormal']:.2f}"]
    path.write_text("\n".join(L) + "\n", encoding="utf8")


def plot(r, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = list(r["leakage"])
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x - 0.2, [r["leakage"][n]["random"]["summary"]["accuracy"][0] for n in names], 0.4, label="random split")
    ax.bar(x + 0.2, [r["leakage"][n]["grouped"]["summary"]["accuracy"][0] for n in names], 0.4, label="grouped split")
    ax.set_xticks(x, names, rotation=15, ha="right")
    ax.set_ylabel("accuracy")
    ax.set_ylim(0, 1.05)
    ax.axhline(0.5, ls=":", c="grey")
    ax.legend()
    ax.set_title("Effect of recording-level leakage")
    fig.tight_layout()
    fig.savefig(out / "leakage.png", dpi=200)


if __name__ == "__main__":
    main()
