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



def main():
    path_input_img = "../data/anae_small.jfif"
    arr_img = cv2.imread(path_input_img, flags=0)  
    arr_img = scale_down(arr_img)



if __name__ == "__main__":
    main()

