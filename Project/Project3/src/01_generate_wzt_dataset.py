import argparse
import os
from pathlib import Path
import random
import cv2
import numpy as np
import pandas as pd

IMG_SIZE = 120

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def draw_wzt5_stimulus(img, thickness=2):
    # WZT stimulus 5: two oblique lines implying tension/conflict.
    cv2.line(img, (34, 78), (52, 60), 0, thickness)
    cv2.line(img, (66, 56), (84, 74), 0, thickness)
    return img

def jitter_point(p, amount=4):
    return (int(p[0] + random.randint(-amount, amount)), int(p[1] + random.randint(-amount, amount)))

def draw_polyline(img, points, color=0, thickness=2, broken=False):
    pts = [jitter_point(p, 3) for p in points]
    if broken:
        for i in range(len(pts) - 1):
            if random.random() < 0.65:
                cv2.line(img, pts[i], pts[i+1], color, thickness)
    else:
        for i in range(len(pts) - 1):
            cv2.line(img, pts[i], pts[i+1], color, thickness)

def add_hand_noise(img, amount=0.015):
    noise_mask = np.random.rand(*img.shape) < amount
    img[noise_mask] = np.random.randint(170, 255, size=noise_mask.sum())
    return img

def add_paper_texture(img):
    # 종이 질감: 완전 흰 배경을 살짝 회색/불균일하게 만든다.
    paper = np.random.normal(loc=248, scale=random.uniform(2, 7), size=img.shape)
    paper = np.clip(paper, 225, 255).astype(np.uint8)
    img = np.minimum(img, paper)

    # 아주 약한 스캔 얼룩
    if random.random() < 0.45:
        for _ in range(random.randint(1, 4)):
            cx = random.randint(10, IMG_SIZE - 10)
            cy = random.randint(10, IMG_SIZE - 10)
            radius = random.randint(8, 25)
            color = random.randint(225, 245)
            cv2.circle(img, (cx, cy), radius, color, -1)
            img = cv2.GaussianBlur(img, (3, 3), 0)

    return img


def random_shift(img, max_shift=6):
    # 그림 전체가 종이 중앙에서 살짝 벗어나는 효과
    dx = random.randint(-max_shift, max_shift)
    dy = random.randint(-max_shift, max_shift)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (IMG_SIZE, IMG_SIZE), borderValue=255)


def degrade_drawing(img):
    # 정상 그림도 약하거나 흔들리게 보이도록 일부 stroke를 흐리게 만든다.
    if random.random() < 0.5:
        img = cv2.GaussianBlur(img, (3, 3), 0)

    if random.random() < 0.4:
        noise = np.random.normal(0, random.uniform(2, 8), img.shape)
        img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    if random.random() < 0.35:
        mask = np.random.rand(*img.shape) < random.uniform(0.003, 0.015)
        img[mask] = np.random.randint(180, 255, size=mask.sum())

    return img

def generate_non_depressed():
    img = np.full((IMG_SIZE, IMG_SIZE), 255, dtype=np.uint8)
    draw_wzt5_stimulus(img, thickness=random.choice([2, 3]))

    motif = random.choice(["star", "flower", "house", "balanced_lines"])
    thickness = random.choice([2, 3])
    if motif == "star":
        center = (60 + random.randint(-5, 5), 60 + random.randint(-5, 5))
        pts = [(60,25),(70,50),(98,50),(75,66),(85,95),(60,76),(35,95),(45,66),(22,50),(50,50),(60,25)]
        draw_polyline(img, pts, thickness=thickness)
    elif motif == "flower":
        cv2.circle(img, (60, 58), 8, 0, thickness)
        for angle in np.linspace(0, 2*np.pi, 6, endpoint=False):
            x = int(60 + 23*np.cos(angle))
            y = int(58 + 23*np.sin(angle))
            cv2.ellipse(img, (x, y), (10, 16), int(np.degrees(angle)), 0, 360, 0, thickness)
        cv2.line(img, (60,66), (60,98), 0, thickness)
        cv2.ellipse(img, (49,83), (12,6), 35, 0, 360, 0, thickness)
    elif motif == "house":
        draw_polyline(img, [(35,70),(60,42),(85,70),(85,98),(35,98),(35,70)], thickness=thickness)
        cv2.rectangle(img, (54,78), (66,98), 0, thickness)
        cv2.rectangle(img, (42,75), (52,85), 0, thickness)
        cv2.rectangle(img, (69,75), (79,85), 0, thickness)
    else:
        for offset in [-18, -6, 6, 18]:
            draw_polyline(img, [(35, 60+offset), (85, 60+offset)], thickness=thickness)
        cv2.circle(img, (60,60), 25, 0, thickness)

        # 정상군도 항상 깨끗하고 완성도 높게 보이지 않도록 만든다.
    if random.random() < 0.45:
        img = degrade_drawing(img)

    img = add_paper_texture(img)
    img = add_hand_noise(img, amount=random.uniform(0.002, 0.010))
    img = cv2.GaussianBlur(img, (3,3), 0)

    return img

def generate_depressed():
    img = np.full((IMG_SIZE, IMG_SIZE), 255, dtype=np.uint8)

    # 우울도 항상 약하고 미완성인 것은 아니게 만든다.
    weak_line_prob = 0.70
    incomplete_prob = 0.65
    blur_prob = 0.55
    normal_like_prob = 0.20

    draw_wzt5_stimulus(img, thickness=random.choice([1, 1, 2]))

    if random.random() < normal_like_prob:
        motif = random.choice(["star", "flower", "house", "balanced_lines"])
    else:
        motif = random.choice(["weak_branch", "unfinished_tree", "fragment", "small_object"])

    if random.random() < weak_line_prob:
        color = random.randint(100, 190)
        thickness = 1
    else:
        color = random.randint(0, 80)
        thickness = random.choice([1, 2])

    broken = random.random() < incomplete_prob

    if motif == "weak_branch":
        draw_polyline(img, [(58,95),(55,75),(52,55),(49,38)],
                      color=color, thickness=thickness, broken=broken)
        for p1, p2 in [((54,65),(35,55)), ((52,52),(72,40)), ((55,78),(76,71))]:
            draw_polyline(img, [p1,p2], color=color, thickness=thickness, broken=broken)
        for _ in range(random.randint(1,4)):
            cv2.ellipse(img, (random.randint(30,90), random.randint(35,80)),
                        (random.randint(6,14), random.randint(10,22)),
                        random.randint(0,160), 0, random.randint(180,330), color, 1)

    elif motif == "unfinished_tree":
        draw_polyline(img, [(62,100),(60,82),(60,64),(61,48)],
                      color=color, thickness=1, broken=broken)
        for _ in range(random.randint(2, 4)):
            x = random.randint(38,85)
            y = random.randint(38,70)
            cv2.ellipse(img, (x,y), (random.randint(8,16), random.randint(14,25)),
                        random.randint(0,180), 0, random.randint(160,330), color, 1)

    elif motif == "fragment":
        for _ in range(random.randint(5,12)):
            p = (random.randint(35,85), random.randint(35,90))
            q = (p[0]+random.randint(-18,18), p[1]+random.randint(-18,18))
            if random.random() < 0.7:
                cv2.line(img, p, q, color, 1)

    elif motif == "small_object":
        cx, cy = random.randint(45,75), random.randint(45,75)
        cv2.circle(img, (cx,cy), random.randint(7,14), color, 1)
        if random.random() < 0.5:
            cv2.line(img, (cx,cy+10), (cx,cy+35), color, 1)

    elif motif == "star":
        pts = [(60,25),(70,50),(98,50),(75,66),(85,95),
               (60,76),(35,95),(45,66),(22,50),(50,50),(60,25)]
        draw_polyline(img, pts, color=color, thickness=thickness, broken=broken)

    elif motif == "flower":
        cv2.circle(img, (60, 58), 8, color, thickness)
        for angle in np.linspace(0, 2*np.pi, 6, endpoint=False):
            x = int(60 + 23*np.cos(angle))
            y = int(58 + 23*np.sin(angle))
            cv2.ellipse(img, (x, y), (10, 16), int(np.degrees(angle)), 0, 360, color, thickness)

    else:
        for offset in [-18, -6, 6, 18]:
            draw_polyline(img, [(35, 60+offset), (85, 60+offset)],
                          color=color, thickness=thickness, broken=broken)
        cv2.circle(img, (60,60), 25, color, thickness)

        # 우울군도 일부는 정상군처럼 비교적 선명하고 완성도 있게 보이도록 만든다.
    if random.random() < 0.30:
        img = cv2.equalizeHist(img)

    if random.random() < blur_prob:
        img = cv2.GaussianBlur(img, (3,3), 0)

    img = add_paper_texture(img)
    img = add_hand_noise(img, amount=random.uniform(0.004, 0.018))

    return img

def augment(img):
    angle = random.uniform(-10, 10)
    scale = random.uniform(0.88, 1.10)

    M = cv2.getRotationMatrix2D((IMG_SIZE/2, IMG_SIZE/2), angle, scale)
    img = cv2.warpAffine(img, M, (IMG_SIZE, IMG_SIZE), borderValue=255)

    if random.random() < 0.55:
        img = random_shift(img, max_shift=7)

    if random.random() < 0.45:
        img = cv2.GaussianBlur(img, (3,3), 0)

    if random.random() < 0.35:
        alpha = random.uniform(0.85, 1.15)
        beta = random.randint(-8, 8)
        img = np.clip(alpha * img + beta, 0, 255).astype(np.uint8)

    return img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/synthetic_wzt")
    parser.add_argument("--n_depressed", type=int, default=600)
    parser.add_argument("--n_non_depressed", type=int, default=600)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    out = Path(args.out)
    dep_dir = out / "depressed"
    non_dir = out / "non_depressed"
    ensure_dir(dep_dir); ensure_dir(non_dir)

    rows = []
    label_noise_prob = 0.10

    for label_name, n, gen_fn, label in [
        ("depressed", args.n_depressed, generate_depressed, 1),
        ("non_depressed", args.n_non_depressed, generate_non_depressed, 0),
    ]:
        for i in range(n):
            img = augment(gen_fn())

            final_label = label
            final_label_name = label_name

            # 실제 심리 데이터의 애매한 경계를 흉내 내기 위한 label noise
            if random.random() < label_noise_prob:
                final_label = 1 - label
                final_label_name = "depressed" if final_label == 1 else "non_depressed"

            fname = f"{label_name}_{i:05d}.png"
            path = out / label_name / fname

            cv2.imwrite(str(path), img)

            rows.append({
                "filename": str(path),
                "label": final_label,
                "label_name": final_label_name,
                "original_rule_label": label,
                "original_rule_label_name": label_name,
                "label_noise": int(final_label != label),
                "source": "synthetic_wzt5_realistic_rule_based",
                "stimulus": "WZT_5"
            })

    pd.DataFrame(rows).to_csv(out / "metadata.csv", index=False)
    print(f"Saved {len(rows)} images to {out}")
    print(f"Metadata: {out / 'metadata.csv'}")

if __name__ == "__main__":
    main()
