import cv2, random, argparse, os

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=None)
ap.add_argument("--slots", type=int, default=1)   # 1 = single marker, 3 = three markers
a = ap.parse_args()

rng = random.Random(a.seed)
tex = os.path.expanduser("~/drone_challenge/models/obstacles/materials/textures")
os.makedirs(tex, exist_ok=True)
d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

ids = rng.sample([1, 2, 3], a.slots)
for k, i in enumerate(ids, 1):
    img = cv2.aruco.generateImageMarker(d, i, 600)
    img = cv2.copyMakeBorder(img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite(f"{tex}/marker_slot{k}.png", img)

print(f"ids per slot = {ids}   TARGET bullseye = {ids[-1]}")