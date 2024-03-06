import numpy as np
import matplotlib.pyplot as plt

import cv2

import pdb

def shitty_edge_detection(path_img:str) -> np.ndarray:
    """Apply edge detection on a given image.
    First use Gauss blur to reduce noice, then use Canny to extract edges.
 
            Parameters:
                    path_img (str): path to the image.
 
            Returns:
                    edges (np.ndarray): arrray of two dimensions. 
                    Row number = height of image,
                    column number = width of image.
                    If a pixel is detected as edge, the value is 255. Else it's 0.
    """
    img = cv2.imread(path_img, flags=0)  
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0) 
    # Canny Edge Detection
    # Default: threshold1=100, threshold2=200
    edges = cv2.Canny(image=img_blur, threshold1=40, threshold2=140, apertureSize=3, L2gradient=False)
    # Uncomment to inspect the image
    #cv2.imshow('edge detection', edges)
    #cv2.waitKey()
    return edges



def array2scatter(edges:np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.where(edges > 250)



def smash_on_plane_xz(edges):
    zs, xs = array2scatter(edges)
    ys = np.zeros(len(zs), dtype=int)
    return xs, ys, np.flip(zs)



def main():
    path_img = "../data/anae_small.jfif"
    edges = shitty_edge_detection(path_img)
    xs, ys, zs = smash_on_plane_xz(edges)
    # Prepare for plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs, ys, zs, marker='.')
    plt.show()
    cv2.destroyAllWindows() 



if __name__ == "__main__":
    main()

