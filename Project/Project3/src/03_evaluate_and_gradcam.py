import argparse
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

IMG_SIZE = 120

def load_img_array(path):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    arr = img.astype("float32") / 255.0
    return arr[None, :, :, None], img

def make_gradcam(model, img_array, layer_name="last_conv"):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if predictions.shape[-1] == 2:
            class_idx = tf.argmax(predictions[0])
            loss = predictions[:, class_idx]
        else:
            loss = predictions[:, 0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = np.maximum(heatmap, 0)
    if np.max(heatmap) != 0:
        heatmap /= np.max(heatmap)
    return heatmap

def overlay_heatmap(original_gray, heatmap):
    heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
    heatmap_uint = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap_uint, cv2.COLORMAP_JET)
    original_bgr = cv2.cvtColor(original_gray, cv2.COLOR_GRAY2BGR)
    overlay = cv2.addWeighted(original_bgr, 0.65, heatmap_color, 0.35, 0)
    return overlay

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/synthetic_wzt")
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", default="results")
    parser.add_argument("--n", type=int, default=12)
    args = parser.parse_args()

    out = Path(args.out) / "gradcam"
    out.mkdir(parents=True, exist_ok=True)

    model = tf.keras.models.load_model(args.model)
    meta = pd.read_csv(Path(args.data) / "metadata.csv").sample(args.n, random_state=42)

    for i, row in enumerate(meta.itertuples()):
        arr, gray = load_img_array(row.filename)
        heatmap = make_gradcam(model, arr)
        overlay = overlay_heatmap(gray, heatmap)
        cv2.imwrite(str(out / f"gradcam_{i:02d}_{row.label_name}.png"), overlay)

    print(f"Saved Grad-CAM images to {out}")

if __name__ == "__main__":
    main()
