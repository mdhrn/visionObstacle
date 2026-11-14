import cv2, os
ROOT = os.path.expanduser("~/drone_challenge/models")
SIZE = 0.30                                    # marker side in metres
d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

CONFIG = """<?xml version="1.0"?>
<model><name>aruco_{i}</name><version>1.0</version>
<sdf version="1.9">model.sdf</sdf></model>
"""
SDF = """<sdf version="1.9">
  <model name="aruco_{i}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry><box><size>{s} {s} 0.002</size></box></geometry>
        <material>
          <diffuse>1 1 1 1</diffuse>
          <specular>0 0 0 1</specular>
          <pbr><metal>
            <albedo_map>model://aruco_{i}/materials/textures/aruco_{i}.png</albedo_map>
            <roughness>1.0</roughness>
            <metalness>0.0</metalness>
          </metal></pbr>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
for i in (1, 2, 3):
    base = f"{ROOT}/aruco_{i}"
    os.makedirs(f"{base}/materials/textures", exist_ok=True)
    img = cv2.aruco.generateImageMarker(d, i, 600)
    img = cv2.copyMakeBorder(img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite(f"{base}/materials/textures/aruco_{i}.png", img)
    open(f"{base}/model.config", "w").write(CONFIG.format(i=i))
    open(f"{base}/model.sdf", "w").write(SDF.format(i=i, s=SIZE))
print("done")