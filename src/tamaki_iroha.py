"""Transform image to matrice. Each pixel becomes a matrix of 3*3"""
import numpy as np
import copy
import cv2
import matplotlib.pyplot as plt
import pyvista
from image_to_array import smash_on_plane
import pdb




def scale_down(arr_img:np.ndarray) -> np.ndarray:
    """Calculate the level of each pixel.
 
            Parameters:
                    arr_img (np.ndarray): array of image in greyscale.
 
            Returns:
                    arr_img (np.ndarray): array scaled down.
                    By default there are 6 levels in total, 
                    so the output array is composed by int between 1 and 6 (included).
    """
    notch = 255 / 6
    return arr_img // notch + 1



def doppel(arr_img:np.ndarray) -> np.ndarray:
    """沈黙のドッペル !! Transform magical girl into doppel.
    The resulting array's size will be three times bigger than the original array.
 
            Parameters:
                    arr_img (np.ndarray): array of image.
 
            Returns:
                    arr_res (np.ndarray): array in "doppel" mode.
    """
    # The key of dict_doppel: 1 is the darkest, 6 is the lightest.
    # In the 3*3 array, 1 corresponds to a dark pixel, 0 corresponds to a light pixel.
    dict_doppel = {}
    dict_doppel[1] = np.ones((3,3))
    dict_doppel[2] = np.array(([1,0,1], [0,1,0], [1,0,1]))
    dict_doppel[3] = np.array(([0,1,0], [1,0,1], [0,1,0]))
    dict_doppel[4] = np.array(([0,0,0], [1,1,1], [0,0,0]))
    dict_doppel[5] = np.array(([0,0,0], [0,1,0], [0,0,0]))
    dict_doppel[6] = np.zeros((3,3))
    # Initialize result array
    arr_res = np.zeros((arr_img.shape[0]*3, arr_img.shape[1]*3))
    # iterate through each unique value in arr_img
    for i in np.unique(arr_img):
        arr_img_clone = copy.deepcopy(arr_img)
        # only keep i, set others to 0
        arr_img_clone[np.where(arr_img_clone!=i)] = 0
        arr_img_clone[np.where(arr_img_clone==i)] = 1
        arr_res += np.kron(arr_img_clone, dict_doppel[i])
    # write to txt to inspect it
    #str_res = ""
    #for row_arr in arr_res:
    #    for col in row_arr:
    #        if col == 0:
    #            str_res += " "
    #        else:
    #            str_res += "@"
    #    str_res += "\n"
    #with open("out.txt", "w") as txt:
    #    txt.write(str_res)
    return arr_res



def main():
    path_input_img = "../data/anae_small.jfif"
    arr_img = cv2.imread(path_input_img, flags=0)  
    arr_img = cv2.flip(arr_img, 0)
    arr_img = scale_down(arr_img)
    arr_res = doppel(arr_img)

    zs, xs = np.where(arr_res==1)
    arr_coordinates = np.array([xs, np.zeros(len(xs)), zs])
    arr_coordinates = (arr_coordinates - arr_coordinates.min())/arr_coordinates.max()
    arr_coordinates = np.transpose(arr_coordinates)

    pdata = pyvista.PolyData(arr_coordinates)
    pdata['orig_sphere'] = np.arange(arr_coordinates.shape[0])
    # create many spheres from the point cloud
    sphere = pyvista.Sphere(radius=0.001, phi_resolution=10, theta_resolution=10)
    pc = pdata.glyph(scale=False, geom=sphere, orient=False)
    pc.plot(cmap='Reds')
    breakpoint()



if __name__ == "__main__":
    main()

