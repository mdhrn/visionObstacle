import math, random, argparse, os

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=None)
a = ap.parse_args()
seed = a.seed if a.seed is not None else random.randrange(10**6)
rng = random.Random(seed)

# ---- paste from the Blender script ----
POSE = (6.3300, 14.7530, 0.6300, -1.5708, 1.5708, 0.0000)
SIZE = 0.5000
# -----------------------------------------

DRONE = "model://iris_with_ardupilot"   # swap for your own drone model

pick = rng.choice([1, 2, 3])
x, y, z, rr, pp, yy = POSE
markers = f"""
    <model name="aruco_marker">
      <static>true</static>
      <pose>{x:.4f} {y:.4f} {z:.4f} {rr:.4f} {pp:.4f} {yy:.4f}</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>{SIZE:.4f} {SIZE:.4f} 0.002</size></box></geometry>
          <material>
            <diffuse>1 1 1 1</diffuse>
            <specular>0 0 0 1</specular>
            <pbr><metal>
              <albedo_map>model://aruco_{pick}/materials/textures/aruco_{pick}.png</albedo_map>
              <roughness>1.0</roughness>
              <metalness>0.0</metalness>
            </metal></pbr>
          </material>
        </visual>
      </link>
    </model>"""
ids = [pick]

world = f"""<?xml version="1.0"?>
<sdf version="1.9">
  <world name="challenge">
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <plugin filename="gz-sim-imu-system" name="gz::sim::systems::Imu"/>
    <plugin filename="gz-sim-navsat-system" name="gz::sim::systems::NavSat"/>

    <spherical_coordinates>
      <surface_model>EARTH_WGS84</surface_model>
      <latitude_deg>-7.7956</latitude_deg>
      <longitude_deg>110.3695</longitude_deg>
      <elevation>100</elevation>
      <heading_deg>0</heading_deg>
    </spherical_coordinates>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <specular>0.3 0.3 0.3 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="c"><geometry><plane><normal>0 0 1</normal><size>200 200</size></plane></geometry></collision>
        <visual name="v">
          <geometry><plane><normal>0 0 1</normal><size>200 200</size></plane></geometry>
          <material><ambient>0.5 0.5 0.5 1</ambient><diffuse>0.5 0.5 0.5 1</diffuse></material>
        </visual>
      </link>
    </model>

    <include>
      <uri>model://obstacles</uri>
      <name>obstacles</name>
      <pose>0 0 0 0 0 0</pose>
    </include>


    <include>
      <uri>{DRONE}</uri>
      <pose>0 0 0.195 0 0 0</pose>
    </include>
  </world>
</sdf>
"""
out = os.path.expanduser("~/drone_challenge/worlds/challenge.sdf")
open(out, "w").write(world)
print(f"seed={seed} order(slot1..3)={ids} -> {out}")
