# Tractor sound classification: leakage-aware results

295 clips; cross-validation uses 40 pseudo-recording groups.

| Model | Acc (random split) | Acc (grouped) | F1 (grouped) | ROC-AUC (grouped) | F1 95% CI |
|---|---|---|---|---|---|
| SVM (RBF) | 0.935 ± 0.034 | 0.807 ± 0.117 | 0.762 ± 0.228 | 0.922 ± 0.070 | [0.76, 0.85] |
| KNN (k=5) | 0.909 ± 0.035 | 0.680 ± 0.192 | 0.683 ± 0.238 | 0.763 ± 0.141 | [0.59, 0.71] |
| Simple CNN | 0.924 ± 0.032 | 0.832 ± 0.051 | 0.745 ± 0.177 | 0.898 ± 0.090 | [0.77, 0.87] |
| ResNet-like CNN (scratch) | 0.945 ± 0.033 | 0.939 ± 0.033 | 0.917 ± 0.063 | 0.959 ± 0.052 | [0.90, 0.96] |

## Accuracy vs group granularity (SVM)

| groups/class | accuracy |
|---|---|
| 5 | 0.763 ± 0.170 |
| 10 | 0.881 ± 0.117 |
| 20 | 0.840 ± 0.044 |
| 40 | 0.910 ± 0.061 |
| 70 | 0.929 ± 0.055 |

## Own phone recordings (6 abnormal clips, never used in training)

SVM recall: 0.00; mean P(abnormal): 0.43
