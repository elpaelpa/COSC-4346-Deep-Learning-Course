import cv2, os, glob
import numpy as np

SRC = "Corn_Project_Data"
OUT = "frames"
SMALL_W, SMALL_H = 640, 360
MOVE_FRAC = 0.5       # save when the view has slid this fraction of the frame width
MIN_SHARP = 50.0        # Laplacian variance; below this, the frame counts as blurry

def shift_between(prev_gray, gray):
    # Track corners from the old frame into the new one, then fit one camera shift to them
    pts_old = cv2.goodFeaturesToTrack(prev_gray, 300, 0.01, 8)
    if pts_old is None:
        return 0.0
    pts_new, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts_old, None)
    found = status.ravel() == 1
    if found.sum() < 10:
        return 0.0
    M, _ = cv2.estimateAffinePartial2D(pts_old[found], pts_new[found], method=cv2.RANSAC)
    return 0.0 if M is None else float(np.hypot(M[0, 2], M[1, 2]))

for vid in sorted(glob.glob(f"{SRC}/*/*.MP4")):
    height = os.path.basename(os.path.dirname(vid))       # camera_2_feet / camera_4_feet
    name = os.path.splitext(os.path.basename(vid))[0]
    os.makedirs(f"{OUT}/{height}", exist_ok=True)

    cap = cv2.VideoCapture(vid)
    prev, moved, i, saved = None, SMALL_W * MOVE_FRAC, 0, 0   # start "full" so the first frame is saved
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(cv2.resize(frame, (SMALL_W, SMALL_H)), cv2.COLOR_BGR2GRAY)
        if prev is not None:
            moved += shift_between(prev, gray)
        if moved >= SMALL_W * MOVE_FRAC and cv2.Laplacian(gray, cv2.CV_64F).var() > MIN_SHARP:
            cv2.imwrite(f"{OUT}/{height}/{name}_f{i:06d}.jpg", frame)
            moved, saved = 0, saved + 1
        prev = gray
        i += 1
    print(f"{vid}: {i} frames, saved {saved}")
