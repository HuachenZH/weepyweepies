import numpy as np
import matplotlib.pyplot as plt

import cv2

import pdb

def shitty_edge_detection(path_img:str) -> np.ndarray:
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



def main():
    path_img = "../data/anae.jfif"
    shitty_edge_detection(path_img)
    cv2.destroyAllWindows() 



if __name__ == "__main__":
    main()

