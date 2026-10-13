import cv2, os, glob, re, sys
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else "labels_export/corn_train"   # unzipped "YOLO with Images" export
OUT = sys.argv[2] if len(sys.argv) > 2 else "label_viz/train"
COLOR = (0, 0, 255)     # BGR red
THICK = 5

os.makedirs(OUT, exist_ok=True)
for img_path in sorted(glob.glob(f"{SRC}/images/*.jpg")):
    stem = os.path.splitext(os.path.basename(img_path))[0]
    name = re.sub(r"^[0-9a-f]{8}-", "", stem)                 # drop Label Studio's upload prefix
    img = cv2.imread(img_path)
    H, W = img.shape[:2]

    # YOLO rows: class cx cy w h, normalized to 0-1; convert to pixel corners
    label_path = f"{SRC}/labels/{stem}.txt"
    rows = np.loadtxt(label_path, ndmin=2) if os.path.getsize(label_path) else np.empty((0, 5))
    for _, cx, cy, w, h in rows:
        x0, y0 = int((cx - w / 2) * W), int((cy - h / 2) * H)
        x1, y1 = int((cx + w / 2) * W), int((cy + h / 2) * H)
        cv2.rectangle(img, (x0, y0), (x1, y1), COLOR, THICK)
        cv2.putText(img, "corn_ear", (x0, max(30, y0 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR, 2)

    title = f"{name}  ({len(rows)} boxes)"
    cv2.putText(img, title, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 0), 9)          # black outline
    cv2.putText(img, title, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3)
    cv2.imwrite(f"{OUT}/{name}.jpg", img)

print(f"drew {len(glob.glob(f'{OUT}/*.jpg'))} images into {OUT}")
