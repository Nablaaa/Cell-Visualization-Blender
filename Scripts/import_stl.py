import bpy
import glob
import os
import numpy as np

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)


all_folders_path = 'Desktop/Run-Pipeline-pos29/Meshes/'

#foldernames = [os.path.basename(fn) for fn in glob.glob(all_folders_path + '*')]
#print(foldernames)


for folder in np.arange(10):
    folder = str(folder).zfill(3)
    filepath = 'Desktop/Run-Pipeline-pos29/Meshes/' + folder + '/'


    filenames = [os.path.basename(fn) for fn in glob.glob(filepath + '*')]


    for fn in filenames:
        print(filepath + fn)
        bpy.ops.import_mesh.stl(filepath=filepath+fn)
        
        translate_x = int(folder) * 55
        
        bpy.ops.transform.translate(value=(translate_x, 0, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


