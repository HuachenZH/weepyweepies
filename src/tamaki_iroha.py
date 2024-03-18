"""Transform image to matrice. Each pixel becomes a matrix of 3*3"""
import numpy as np
import copy
import cv2
import matplotlib.pyplot as plt
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
    """沈黙のドッペル !! Transform magical girl into doppel"""
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
    breakpoint()



def main():
    path_input_img = "../data/anae_small.jfif"
    arr_img = cv2.imread(path_input_img, flags=0)  
    arr_img = scale_down(arr_img)
    doppel(arr_img)



if __name__ == "__main__":
    main()

