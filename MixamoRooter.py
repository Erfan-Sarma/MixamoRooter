bl_info = {
    "name": "MixamoRooter",
    "author": "Erfan-Sarma",
    "version": (1, 5),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > MixamoRooter",
    "description": "Injects root bone, maps Hips/Root channels, and fixes loop snapping for active Mixamo characters and animations in UE5",
    "category": "Animation",
}

import bpy

class MIXAMO_OT_FixCharacter(bpy.types.Operator):
    bl_idname = "mixamo.fix_character"
    bl_label = "Fix Character Mesh/Skeleton"
    bl_description = "Injects a root bone at world origin and parents the Hips bone to it"

    def execute(self, context):
        if bpy.context.object and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        armature = bpy.context.active_object

        if armature and armature.type == 'ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = armature.data.edit_bones
            
            hips_name = next((b.name for b in edit_bones if 'hips' in b.name.lower()), None)
            
            if hips_name:
                hips_bone = edit_bones.get(hips_name)
                
                if 'root' in edit_bones:
                    edit_bones.remove(edit_bones.get('root'))
                    
                root_bone = edit_bones.new('root')
                root_bone.head = (0.0, 0.0, 0.0)
                root_bone.tail = (0.0, 0.0, 1.0)
                hips_bone.parent = root_bone
                
                bpy.ops.object.mode_set(mode='OBJECT')
                self.report({'INFO'}, "SUCCESS: Root bone added to character skeleton!")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Hips bone not found in armature.")
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, "Please select an Armature object first.")
            return {'CANCELLED'}


class MIXAMO_OT_FixAnimation(bpy.types.Operator):
    bl_idname = "mixamo.fix_animation"
    bl_label = "Fix Animation Root Motion"
    bl_description = "Maps Hips X -> Root X, Hips Z -> Root Y, and fixes hip loop snapping for Unreal Engine"

    def execute(self, context):
        if bpy.context.object and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        armature = bpy.context.active_object

        if armature and armature.type == 'ARMATURE':
            # 1. Edit Mode: Create Root Bone
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = armature.data.edit_bones
            
            hips_name = next((b.name for b in edit_bones if 'hips' in b.name.lower()), None)
            
            if hips_name:
                hips_bone = edit_bones.get(hips_name)
                
                if 'root' in edit_bones:
                    edit_bones.remove(edit_bones.get('root'))
                    
                root_bone = edit_bones.new('root')
                root_bone.head = (0.0, 0.0, 0.0)
                root_bone.tail = (0.0, 0.0, 1.0)
                hips_bone.parent = root_bone
                
                # 2. Pose Mode: Map Animation Curves
                bpy.ops.object.mode_set(mode='POSE')
                action = armature.animation_data.action if armature.animation_data else None
                
                if action:
                    start_f = int(action.frame_range[0])
                    end_f = int(action.frame_range[1])
                    context.scene.frame_start = start_f
                    context.scene.frame_end = end_f
                    
                    hips_path = f'pose.bones["{hips_name}"].location'
                    root_path = 'pose.bones["root"].location'
                    
                    def get_or_create_fcurve(path, index):
                        if hasattr(action, "fcurve_ensure_for_datablock"):
                            return action.fcurve_ensure_for_datablock(armature, path, index=index)
                        else:
                            return action.fcurves.find(path, index=index) or action.fcurves.new(path, index=index)

                    fc_hips_x = get_or_create_fcurve(hips_path, 0)
                    fc_hips_y = get_or_create_fcurve(hips_path, 1)
                    fc_hips_z = get_or_create_fcurve(hips_path, 2)
                    
                    fc_root_x = get_or_create_fcurve(root_path, 0)
                    fc_root_y = get_or_create_fcurve(root_path, 1)
                    
                    # Transfer Hips X -> Root X
                    if fc_hips_x and len(fc_hips_x.keyframe_points) > 0 and fc_root_x:
                        fc_root_x.keyframe_points.clear()
                        for pt in fc_hips_x.keyframe_points:
                            fc_root_x.keyframe_points.insert(pt.co[0], pt.co[1])
                        fc_hips_x.keyframe_points.clear()
                        fc_hips_x.keyframe_points.insert(float(start_f), 0.0)
                        
                    # Transfer Hips Z -> Root Y
                    if fc_hips_z and len(fc_hips_z.keyframe_points) > 0 and fc_root_y:
                        fc_root_y.keyframe_points.clear()
                        for pt in fc_hips_z.keyframe_points:
                            fc_root_y.keyframe_points.insert(pt.co[0], pt.co[1])
                        fc_hips_z.keyframe_points.clear()
                        fc_hips_z.keyframe_points.insert(float(start_f), 0.0)
                        
                    # Fix Hips Y location loop snapping
                    if fc_hips_y and len(fc_hips_y.keyframe_points) > 1:
                        first_val = fc_hips_y.keyframe_points[0].co[1]
                        fc_hips_y.keyframe_points[-1].co[1] = first_val
                        
                    action.update_tag()
                    bpy.context.view_layer.update()
                    self.report({'INFO'}, "SUCCESS: Animation root motion and hip loop fixed!")
                    return {'FINISHED'}
                else:
                    self.report({'WARNING'}, "Root bone created, but no action found on armature.")
                    return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Hips bone not found.")
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, "Please select an Armature object first.")
            return {'CANCELLED'}


class VIEW3D_PT_MixamoRootPanel(bpy.types.Panel):
    bl_label = "MixamoRooter"
    bl_idname = "VIEW3D_PT_mixamo_root_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MixamoRooter"

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Step 1: Character Setup", icon='ARMATURE_DATA')
        layout.operator("mixamo.fix_character", icon='BONE_DATA')
        
        layout.separator()
        
        layout.label(text="Step 2: Animation Setup", icon='ACTION')
        layout.operator("mixamo.fix_animation", icon='ANIM_DATA')


classes = (
    MIXAMO_OT_FixCharacter,
    MIXAMO_OT_FixAnimation,
    VIEW3D_PT_MixamoRootPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
