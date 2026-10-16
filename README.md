# MaxamoRooter 

**MaxamoRooter** is a lightweight Blender add-on built to instantly prepare individual Mixamo character meshes and animation sequences for **Unreal Engine 5 (UE5) Root Motion**.

---

## 💡 The Problem It Solves
Mixamo assets do not come with a standard `root` bone, placing all world translation directly onto the `Hips` bone. When brought into Unreal Engine, this prevents character root motion from driving movement correctly and breaks animation retargeting. 

**MaxamoRooter** provides quick one-click panel controls directly inside Blender to inject the missing root bone and map animation channels properly.

---

## ✨ Features
*   **Character Setup:** Instantly generates a `root` bone at the world origin (`0,0,0`) and parents the `Hips` bone beneath it.
*   **Animation Curve Mapping:** Remaps keyframes cleanly (Hips X $\rightarrow$ Root X, Hips Z $\rightarrow$ Root Y) to establish proper root motion tracks for UE5.
*   **Convenient UI Panel:** Easily accessible right from the 3D Viewport sidebar (`N-Panel > MaxamoRooter`).

---

## 📥 Installation

1. Download or clone this repository and grab the python file.
2. Open Blender (v4.0 or newer).
3. Go to **Edit > Preferences > Add-ons**.
4. Click the install dropdown/button in the top right, select the script file, and click **Install Add-on**.
5. Enable **MaxamoRooter** in your add-on list.

---

## 🎮 How to Use

1. Import your raw Mixamo FBX file into Blender.
2. Select your character's Armature object in the 3D Viewport.
3. Press **N** to open the sidebar and navigate to the **MaxamoRooter** tab.
4. Click **Fix Character Mesh/Skeleton** (for meshes) or **Fix Animation Root Motion** (for animations).
5. Export your asset back out to FBX and import it straight into Unreal Engine 5!

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
