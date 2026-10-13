import os, glob, shutil
from collections import defaultdict
import numpy as np

SRC = "frames"
OUT = "to_label"
# Every 5th video per height, so validation spans the whole recording session
VAL_VIDEOS = {"GOPR0169", "GOPR0174", "GOPR0179", "GOPR0184",     # 2 ft
              "GOPR0392", "GOPR0397", "GOPR0402", "GOPR0407"}     # 4 ft
TRAIN_PER_VIDEO = 3     # evenly spaced frames taken from each training video
VAL_STEP = 2            # take every Nth frame from each validation video

# Group extracted frames by source video (filenames look like GOPR0165_f000043.jpg)
by_video = defaultdict(list)
for path in glob.glob(f"{SRC}/*/*.jpg"):
    by_video[os.path.basename(path).split("_")[0]].append(path)

shutil.rmtree(OUT, ignore_errors=True)   # to_label/ is generated output, rebuilt every run
for split in ("train", "val"):
    os.makedirs(f"{OUT}/{split}")

counts = {"train": 0, "val": 0}
for video, paths in sorted(by_video.items()):
    paths.sort()
    if video in VAL_VIDEOS:
        split, picks = "val", paths[::VAL_STEP]
    else:
        idx = np.linspace(0, len(paths) - 1, min(TRAIN_PER_VIDEO, len(paths))).round().astype(int)
        split, picks = "train", [paths[i] for i in idx]
    for p in picks:
        shutil.copy2(p, f"{OUT}/{split}/{os.path.basename(p)}")
    counts[split] += len(picks)

print(f"videos: {len(by_video)}  train: {counts['train']}  val: {counts['val']}")
