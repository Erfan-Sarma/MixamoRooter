# MixamoRooter 🚀

**MixamoRooter** is a lightweight Blender add-on built to instantly prepare individual Mixamo character meshes and animation sequences for **Unreal Engine 5 (UE5) Root Motion**.

---

## 🎯 Motivation & Philosophy
My intention was to simply add the missing `root` bone to Mixamo characters and animations so they are much easier to use in Unreal Engine. Specifically, this allows you to seamlessly retarget external Mixamo animations to standard UE skeletons (like the Mannequin) and use UE-compatible skeletons with external animation libraries. 

For this purpose, the best practice I found was to handle the structural bone injection and channel mapping cleanly inside Blender, and then let Unreal Engine handle the rest via its powerful IK Retargeter system.

---

## ✨ Features
*   **Character Setup:** Instantly generates a `root` bone at the world origin (`0,0,0`) and parents the `Hips` bone beneath it.
*   **Animation Curve Mapping:** Remaps keyframes cleanly (Hips X $\rightarrow$ Root X, Hips Z $\rightarrow$ Root Y) to establish proper root motion tracks for UE5.
*   **Convenient UI Panel:** Easily accessible right from the 3D Viewport sidebar (`N-Panel > MixamoRooter`).

---

## 📦 Looking for Batch Processing?
If you need to process dozens of animations or characters at once, check out the bulk version:
👉 **[MixamoRooter (Bulk) Repository](https://github.com/Erfan-Sarma/Mixamo-Rooter-Bulk.git)**

---

## 📥 Installation

1. Download or clone this repository and grab the python file.
2. Open Blender (v4.0 or newer).
3. Go to **Edit > Preferences > Add-ons**.
4. Click the install button in the top right, select the script file, and click **Install Add-on**.
5. Enable **MixamoRooter** in your add-on list.

---

## 🎮 How to Use

1. Import your raw Mixamo FBX file into Blender.
2. Select your character's Armature object in the 3D Viewport.
3. Press **N** to open the sidebar and navigate to the **MixamoRooter** tab.
4. Click **Fix Character Mesh/Skeleton** (for meshes) or **Fix Animation Root Motion** (for animations).
5. Export your asset back out to FBX and import it straight into Unreal Engine 5!

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
