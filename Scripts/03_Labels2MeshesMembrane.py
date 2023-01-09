"""
Eric Schmidt
eschmidt@mpi-cbg.de
Eric_Schmidt_99@gmx.de

script based on script by Manan Lalit,

use conda environment: conda activate Labels2Meshes


This script converts label images to 3D meshes.

Type in the directory of the label images, the general file name 
and the save directory.

Also change the voxel size 
and the smoothing

a higher smoothing value brings more roundish shapes but also
more vertices in the blender file later.

Additionally in the end of the script is the part for using several 
cores for computing. You can change the CPUs (num_workers) if you
have more than 4 cores.
"""


import tifffile
import numpy as np
from skimage import measure
from tqdm import tqdm
from pyvista import wrap
import trimesh
from glob import glob
from tqdm import tqdm
import pandas as pd
import os
import glob 
import re
from scipy.ndimage import zoom
from skimage.io import imread, imsave
import time
from skimage.measure import regionprops
import matplotlib.patches as mpatches




###############################################################
################## get file names/dir #########################
###############################################################
label_dir = "Merged_Cells/"
file_general_name = 'pos13-T_'

output_dir = 'Meshes-Membrane/'


voxelsize = (0.173*4, 0.173*4, 1) #(x,y,z)
smoothing = 100


# extract all filenames
mask_filenames = [os.path.basename(fn) for fn in glob.glob(label_dir  + '*.tif*')]

# extract all timepoints
t = [int(re.search(file_general_name + '(.*)_predictions', fn).group(1))   for fn in mask_filenames ]

# sort list by time 
t, mask_filenames = zip(*sorted(zip(t, mask_filenames)))

print(mask_filenames, t)




###############################################################
################## create output directory ####################
###############################################################



# create folder if not existent already
try:
    os.mkdir(output_dir)
except FileExistsError :
    pass
    
    

###############################################################
################## make mesh out of label #####################
###############################################################

#@njit(nogil=True) 
def Label2Mesh(mask, mask_id):
	mask_=mask==mask_id
	mask_=np.transpose(mask_, (2, 1, 0))
	verts, faces, n, val = measure.marching_cubes(mask_,  spacing = voxelsize) #TODO
	tmesh = trimesh.Trimesh(verts, faces=faces, process=True) # mesh object
	mesh = wrap(tmesh)
	smooth = mesh.smooth(n_iter=smoothing) # TODO
	
	return smooth


def GoThroughAllFiles(t, fn, label_dir):
		#print("current mask is {}".format(fn))
		#print("read img ...")
		
		mask = tifffile.imread(label_dir + fn).astype(np.uint16)
		
		#print("get ids ...")
		ids = np.unique(mask)
		ids = ids[ids!=0]
		
		
		#print("Ids: ",str(ids))
		#print("create folder for timestep ...")

		try:
			os.mkdir(output_dir + str(t).zfill(3))

		except FileExistsError :
			pass



		#print("go through ids and create masks ...")
		
		for i, mask_id in enumerate(ids):
			print("mask " + str(i) + " out of " + str(len(ids)))
			
			smooth = Label2Mesh(mask[:,::4,::4], mask_id)
			smooth.save(output_dir + str(t).zfill(3)+"/mesh_"+str(mask_id).zfill(3)+".stl")




############################################################################################
###################### This part is for accelerating the process ###########################
############################################################################################


from multiprocessing import Process, current_process
import sys



worker_count = 4

N = len(mask_filenames)
Nsteps = int(N/worker_count)

worker_pool = []
for i in range(worker_count):
	if i < worker_count-1:
		for T, fn in zip(t[i * Nsteps : (i+1) * Nsteps],mask_filenames[i * Nsteps : (i+1) * Nsteps]):	
			print(fn)
			#img_receptor = imread(foldername_receptor + fn_img)
			#img_mask = imread(foldername_mask + fn_mask)

			p = Process(target=GoThroughAllFiles, args=(T, fn, label_dir))
			p.start()
			worker_pool.append(p)
			
	if i == worker_count - 1: # fill the last worker with all files which are not used yet
		for T, fn in zip(t[i * Nsteps : ],mask_filenames[i * Nsteps : ]):	
			print(fn)
			#img_receptor = imread(foldername_receptor + fn_img)
			#img_mask = imread(foldername_mask + fn_mask)
			
			p = Process(target=GoThroughAllFiles, args=(T, fn, label_dir))
			p.start()
			worker_pool.append(p)
    
    
for p in worker_pool:
    p.join()  # Wait for all of the workers to finish.






    
