# 2 Feet

Watched 
- 165,166

# 4 Feet
- 


We could compare track the changes per frame?


# Labeling Rules

Class: `corn_ear` (one class, bounding boxes). Same rules for train and val.
Example: `docs/labeling_example.jpg` (GOPR0395_f000266, two ears boxed).

## Ear vs. leaf
- Ear = fat, rounded 3D spindle that tapers to a tip, with shading. Leaf = flat, thin, long, curls or droops.
- Ear attaches to the stalk at a joint, at an angle, often with a dark tuft of dried silk at the tip.
- Ear is noticeably thicker than the stalk it hangs from.

## Rules
1. Box every corn ear on the nearby plants (left/right edges of the frame), even if partly hidden. Skip ears deep in the tunnel: if shorter than ~1/20 of image height (~55 px on 1080p), skip.
2. Partly hidden: box only the visible part + the stalk joint. Don't guess the hidden part.
3. Include the joint: extend the box to where the ear attaches to the stalk (the target is the ear / ear-stalk connection).
4. Only box things I can tell are ears. If it might just be a leaf, leave it.
5. Zero boxes is a valid label for frames with no visible ears.

## Tips
- Zoom in (scroll wheel); ears that blend in at full view are often obvious zoomed.
- Stuck on a frame -> scrub that part of the source video; ears stand out when the camera moves.


# Anticipated Challenges (for report)
- Late-season dried corn: husked ears are the same tan as dead leaves.
- Heavy occlusion by leaves.
- Forward-facing camera: ears far down the row are tiny, so only nearby ears are labeled; the model may still fire on unlabeled far ears.
- Harsh backlighting from the sky.