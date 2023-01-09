import bpy
import glob
import os
import numpy as np



all_meshes_folder = 'Desktop/Workspace/MPI/Blender/Meshes/'
xyz_path = 'Desktop/Workspace/MPI/Blender/xyz-files/'

xyz_files = [os.path.basename(fn) for fn in glob.glob(xyz_path + '*')]

print(xyz_files)
#foldernames = [os.path.basename(fn) for fn in glob.glob(all_meshes_folder + '*')]




for folder in np.arange(2):
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False, confirm=False)

    print(folder)
    xyz_fn = "pos13-T_" + str(folder) + "_ch_2_backround_removed.xyz"
    
    bpy.ops.import_mesh.xyz(filepath=xyz_path+xyz_fn,scale_ballradius=0.1)
    

    # add light
    spot_pos = (0, 40,0)
    bpy.ops.object.light_add(type='POINT', align='WORLD', location=spot_pos, scale=(1, 1, 1))
    bpy.context.object.data.energy = 1000000 # 1 MW

    # add camera
    camera_pos = (0, 60, 0)
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.5708, 0, 3.14159), scale=(1, 1, 1))
    bpy.ops.transform.translate(value=camera_pos, orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.context.object.data.lens = 61
    bpy.context.scene.camera = bpy.data.objects['Camera']

    # set render
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_x = 1920




    folder = str(folder).zfill(3)
    filepath = all_meshes_folder + folder + '/'

    print(filepath)

    filenames = [os.path.basename(fn) for fn in glob.glob(filepath + '*')]
    
    bpy.context.scene.frame_current = int(folder)

    # set render time frame
    bpy.context.scene.frame_start = int(folder)
    bpy.context.scene.frame_end = int(folder)




    # load filenames for timestep
    print(filenames)
    for fn in filenames:
        print(fn)
        print(filepath + fn)
        bpy.ops.import_mesh.stl(filepath=filepath+fn)
        
        translate_x = - 26
        bpy.ops.transform.translate(value=(translate_x, -26, -26), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        # give them properties
        bpy.ops.object.modifier_add(type='WIREFRAME')
        bpy.context.object.modifiers["Wireframe"].thickness = 0.0003

        # create material
        item = bpy.context.object
        item.data.materials.append(bpy.data.materials["Material"])
     
     
    # now render   
    bpy.ops.render.render(animation=True)
    
 
