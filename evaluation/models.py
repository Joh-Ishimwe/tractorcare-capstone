"""Model factories. Architectures copied from the notebook so results match the deployed design."""
from __future__ import annotations

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def svm():
    return make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, probability=True,
                                               class_weight="balanced", random_state=0))


def knn():
    return make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5, weights="distance"))


class KerasClassifier:
    """Minimal sklearn-style wrapper: fit(X[N,40,100], y) / predict_proba(X) -> P(abnormal)."""

    def __init__(self, builder, epochs=25, batch_size=16, seed=0):
        self.builder, self.epochs, self.batch_size, self.seed = builder, epochs, batch_size, seed

    def fit(self, X, y):
        import tensorflow as tf
        tf.keras.utils.set_random_seed(self.seed)
        tf.keras.backend.clear_session()
        self.model = self.builder(X.shape[1:] + (1,))
        self.model.fit(X[..., None], y, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        return self

    def predict_proba(self, X):
        return self.model.predict(X[..., None], verbose=0).ravel()


def simple_cnn(shape):
    from tensorflow.keras import Sequential, layers
    m = Sequential([layers.Input(shape), layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(2),
                    layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(2), layers.Flatten(),
                    layers.Dense(64, activation="relu"), layers.Dropout(0.5),
                    layers.Dense(1, activation="sigmoid")])
    m.compile("adam", "binary_crossentropy")
    return m


def _res_block(x, filters, stride=1):
    from tensorflow.keras import layers
    y = layers.Conv2D(filters, 3, strides=stride, padding="same", activation="relu")(x)
    y = layers.BatchNormalization()(y)
    y = layers.Conv2D(filters, 3, padding="same")(y)
    y = layers.BatchNormalization()(y)
    if stride != 1 or x.shape[-1] != filters:
        x = layers.BatchNormalization()(layers.Conv2D(filters, 1, strides=stride, padding="same")(x))
    return layers.ReLU()(layers.Add()([x, y]))


def resnet_cnn(shape):
    from tensorflow.keras import Model, layers
    i = layers.Input(shape)
    x = layers.BatchNormalization()(layers.Conv2D(32, 7, strides=2, padding="same", activation="relu")(i))
    x = layers.MaxPooling2D(3, strides=2, padding="same")(x)
    for f, s in [(32, 1), (32, 1), (64, 2), (64, 1)]:
        x = _res_block(x, f, s)
    x = layers.Dropout(0.5)(layers.Dense(64, activation="relu")(layers.GlobalAveragePooling2D()(x)))
    m = Model(i, layers.Dense(1, activation="sigmoid")(x))
    m.compile("adam", "binary_crossentropy")
    return m


def transfer_from(pretrained_path):
    """Freeze all but the last 3 layers of a MIMII-pretrained ResNet and add the notebook's head."""
    def build(shape):
        from tensorflow import keras
        from tensorflow.keras import Sequential, layers
        base = keras.models.load_model(pretrained_path)
        for l in base.layers[:-3]:
            l.trainable = False
        m = Sequential([base, layers.Dense(128, activation="relu"), layers.Dropout(0.3),
                        layers.Dense(1, activation="sigmoid")])
        m.compile(keras.optimizers.Adam(1e-4), "binary_crossentropy")
        return m
    return build
