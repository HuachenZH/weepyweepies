"""Transform image to matrice. Each pixel becomes a matrix of 3*3"""
import numpy as np
import cv2
import pdb




def scale_down(arr_img:np.ndarray) -> np.ndarray:
    """Calculate the level of each pixel.
 
            Parameters:
                    arr_img (np.ndarray): array of image in greyscale.
 
            Returns:
                    arr_img (np.ndarray): array scaled down.
                    By default there are 6 levels in total, 
                    so the output array is composed by int between 0 and 5 (included).
    """
    notch = 255 / 6
    return arr_img // notch



def doppel(arr_img:np.ndarray) -> np.ndarray:
    """沈黙のドッペル !! Transform magical girl into doppel"""
    dict_doppel = {}
    dict_doppel[0] = np.ones((3,3))
    dict_doppel[1] = np.array(([1,0,1], [0,1,0], [1,0,1]))
    dict_doppel[2] = np.array(([0,1,0], [1,0,1], [0,1,0]))
    dict_doppel[3] = np.array(([0,0,0], [1,1,1], [0,0,0]))
    dict_doppel[4] = np.array(([0,0,0], [0,1,0], [0,0,0]))
    dict_doppel[5] = np.zeros((3,3))
    breakpoint()



def main():
    path_input_img = "../data/anae_small.jfif"
    arr_img = cv2.imread(path_input_img, flags=0)  
    arr_img = scale_down(arr_img)
    doppel(arr_img)



if __name__ == "__main__":
    main()

