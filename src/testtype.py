import matplotlib.pyplot as plt
import numpy as np
import cv2

import pdb


def shitty_edge_detection(path_img:str):
    # Read the original image in greyscale
    img = cv2.imread(path_img,flags=0) 
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0) 
    return



def main():
    path_img = "../data/anae.jfif"
    img_edge = shitty_edge_detection(path_img)


if __name__ == "__main__":
    main()