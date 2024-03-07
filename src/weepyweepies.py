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
    # Flip image vertically
    img = cv2.flip(img, 0)
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
    """Extract coordinate of scatter points from an image's array.
 
            Parameters:
                    edges (np.ndarray)): array of the image.
                    The image is in greyscale in black background, all pixels in white,
                    their row and col index will be extracted. 
 
            Returns:
                    (tuple[np.ndarray, np.ndarray]): a tuple of two numpy arrays.
                    The first array is the index of row of white pixels.
                    The second array is the index of column of white pixels.
    """
    return np.where(edges > 250)



def smash_on_plane_xz(edges:np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Project an image onto the xz plane.
 
            Parameters:
                    edges (np.ndarray)): array of the image.
 
            Returns:
                    xs, ys, zs (tuple[np.ndarray, np.ndarray, np.ndarray]): a tuple of three numpy arrays.
                    xs: array of scatter points' x axis coordinate.
                    ys: array of scatter points' y axis coordinate.
                    zs: array of scatter points' z axis coordinate.
                    ----------------
                    xs: (1, 7, 6, 7, 9)
                    ys: (3, 4, 9, 7, 0)
                    zs: (0, 1, 6, 5, 1)
                         ^  Coordinate of the point: (1, 3, 0)
    """
    zs, xs = array2scatter(edges)
    ys = np.zeros(len(zs), dtype=int)
    return xs, ys, zs



def main():
    path_img = "../data/txt_anae.jpg"
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

