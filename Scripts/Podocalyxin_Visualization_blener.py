import bpy
import glob
import os
import re
import time
#load mesh => see old file



Pod_high_mat = bpy.data.materials["Pod_high"]
Pod_low_mat = bpy.data.materials["Pod_low"]


#object = "Sphere"
#object.select_set(True)
def get_progress(total_cells, current_cell, time_passed):
    toal_cells = total_cells+1
    current_cell = current_cell +1
    cells_left=total_cells-current_cell
    time_per_cell=time_passed/current_cell
    time_left=cells_left*time_per_cell
    time_left=time_left/60 # in minutes
    return time_left

all_pod_meshes = 'Meshes-Podocalyxin/'

all_T = sorted([int(os.path.basename(fn)) for fn in glob.glob(all_pod_meshes + '*')])

bpy.ops.object.select_all(action='DESELECT') # deselect everything
  
    
for t in all_T: 
       
    
    folder_t = str(t).zfill(3)
    filepath = all_pod_meshes + folder_t + '/'

    filenames = [os.path.basename(fn) for fn in glob.glob(filepath + '*')]
    
    # load meshes
    for fn in filenames:
        print(fn)
        print(filepath + fn)
        
        bpy.context.scene.frame_set(t) 
        bpy.ops.import_mesh.stl(filepath=filepath+fn)
    
    
        ob = bpy.context.object
        
         
        
        file_general_name ='T_' + folder_t + "_mesh_"
        appendix = ".stl"
        mesh_nr = int(re.search(file_general_name + '(.*)' + appendix, fn).group(1))

        print(mesh_nr)
        
        if mesh_nr == 2:
            ob.data.materials.append(Pod_low_mat)
             
        if mesh_nr == 3:
            ob.data.materials.append(Pod_high_mat)
     
    
        #ob = bpy.data.objects[fn[:-4]]
        #ob = bpy.context.object
        
        
        # the following is a bit strange but it works
        # all meshes will be hidden (except the one for
        # the time frame of interst
        # Than the one of interst will be in "not hidden" state
        # in best case i would only do this once and not for
        # every timestep (to increase performance)
        for hide_t in all_T:
            if hide_t != t:
                ob.hide_render = True
                ob.hide_viewport = True
                ob.keyframe_insert(data_path="hide_render", frame=hide_t)
                ob.keyframe_insert(data_path="hide_viewport", frame=hide_t)
        
        ob.hide_render = False
        ob.hide_viewport = False
        ob.keyframe_insert(data_path="hide_render", frame=t)
        ob.keyframe_insert(data_path="hide_viewport", frame=t)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

all_meshes_folder = 'Meshes/'

foldernames = [os.path.basename(fn) for fn in glob.glob(all_meshes_folder + '*')]




for folder in foldernames:
   
    folder = str(folder).zfill(3)
    filepath = all_meshes_folder + folder + '/'

    filenames = [os.path.basename(fn) for fn in glob.glob(filepath + '*')]
    
    
    print(filenames)
    for fn in filenames:
        bpy.ops.import_mesh.stl(filepath=filepath+fn)

        # give them properties
        bpy.ops.object.modifier_add(type='WIREFRAME')
        bpy.context.object.modifiers["Wireframe"].thickness = 0.0003

     
    # now render   
    bpy.ops.render.render(animation=True)
    
 
            
        