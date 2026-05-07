import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

IMG_SIZE = 120

def load_metadata(data_dir):
    meta = pd.read_csv(Path(data_dir) / "metadata.csv")
    return meta

def load_image(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=1)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img = tf.cast(img, tf.float32) / 255.0
    return img

def make_ds(paths, labels, batch_size=32, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(paths), seed=42)
    ds = ds.map(lambda p, y: (load_image(p), y), num_parallel_calls=tf.data.AUTOTUNE)
    return ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)

def build_model(model_type="softmax"):
    inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 1))
    x = tf.keras.layers.Conv2D(16, (3,3), activation="relu", padding="same")(inputs)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(32, (3,3), activation="relu", padding="same")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(64, (3,3), activation="relu", padding="same", name="last_conv")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.3)(x)

    if model_type == "softmax":
        outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
        loss = "sparse_categorical_crossentropy"
        metrics = ["accuracy"]
    elif model_type == "hinge":
        outputs = tf.keras.layers.Dense(1, activation="linear")(x)
        loss = tf.keras.losses.Hinge()
        metrics = ["accuracy"]
    else:
        raise ValueError("model_type must be softmax or hinge")

    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss=loss, metrics=metrics)
    return model

def convert_labels_for_hinge(y):
    # Hinge expects labels in {-1, 1}
    return np.where(y == 1, 1, -1).astype(np.float32)

def predict_labels(model, ds, model_type):
    raw = model.predict(ds)
    if model_type == "softmax":
        return np.argmax(raw, axis=1)
    return (raw.reshape(-1) >= 0).astype(int)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/synthetic_wzt")
    parser.add_argument("--model_type", choices=["softmax", "hinge"], default="softmax")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    meta = load_metadata(args.data)
    X = meta["filename"].values
    y = meta["label"].values.astype(int)

    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.25, stratify=train_y, random_state=42)

    train_y_fit = convert_labels_for_hinge(train_y) if args.model_type == "hinge" else train_y
    val_y_fit = convert_labels_for_hinge(val_y) if args.model_type == "hinge" else val_y

    train_ds = make_ds(train_x, train_y_fit, shuffle=True)
    val_ds = make_ds(val_x, val_y_fit, shuffle=False)
    test_ds_for_pred = make_ds(test_x, test_y, shuffle=False)

    model = build_model(args.model_type)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(str(out / "model.keras"), monitor="val_accuracy", save_best_only=True)
    ]

    history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)
    pred = predict_labels(model, test_ds_for_pred, args.model_type)

    cm = confusion_matrix(test_y, pred)
    report = classification_report(test_y, pred, target_names=["non_depressed", "depressed"], output_dict=True)

    with open(out / "classification_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    np.savetxt(out / "confusion_matrix.csv", cm, delimiter=",", fmt="%d")
    pd.DataFrame(history.history).to_csv(out / "history.csv", index=False)

    print("Confusion matrix:")
    print(cm)
    print(classification_report(test_y, pred, target_names=["non_depressed", "depressed"]))

if __name__ == "__main__":
    main()
