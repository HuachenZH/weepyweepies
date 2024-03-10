import numpy as np
import matplotlib.pyplot as plt

import cv2

from image_to_array import img2arr

import pdb



def main():
    path_img = "../data/txt_a.jpg"
    xs_img1, ys_img1, zs_img1 = img2arr(path_img, False, "xz")
    path_img = "../data/txt_q.jpg"
    xs_img2, ys_img2, zs_img2 = img2arr(path_img, True, "yz")

    # Prepare for plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs_img1, ys_img1, zs_img1, marker='.')
    ax.scatter(xs_img2, ys_img2, zs_img2, marker='^')
    plt.show()
    #cv2.destroyAllWindows() 



if __name__ == "__main__":
    main()

