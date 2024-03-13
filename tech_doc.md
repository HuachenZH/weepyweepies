# Technical Documentation


## Conventions
Space:
```shell
      ^  z axis
      |
      |
      |
      |
      |
      |
      /---------------------------->  y axis
     /
    /
   /
  /
 /
\/  x axis
```

## Architecture
```shell
[input image] --(image processing)--> [arrays] --(data processing)--> [scatter points] --(visualization)--> ?
```

### Architecture - image processing
Turn image into arrays.  
I think of two ways to do so:  
1. Edge detection.
2. transform a pixel to a matrix of 3x3, points at 0 or 1 depending on the color scale of pixel  

For the first point, __edge detection__, it does not work very well on portraits.  
It also needs some pre processing on images before __edge detection__, for example __gauss blur__ to remove noise on the image.  
There is lots of things that you can configure: 
- More gauss blur leads to less noise on the image, however it would be hard to detect edge. Less gauss blur leaves the edge evident, however it cannot remove much noises.  
  ```python
  img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0) 
  #                                 ^  modify here, it can only be odd numbers
  # The greater the number, the more it will be blurred
  ```
- the threshold of edge detection.
  ```python
  edges = cv2.Canny(image=img_blur, threshold1=40, threshold2=140, apertureSize=3, L2gradient=False)
  # threshold1 is the min value of considering as edge.
  # threshold2 is the max value of considering as edge.
  ```

This step turns image into arrays. Say we have an image of 3*3 pixel:
```shell  
0 0 0
0 0 255
0 0 0
```  
The objective is to smash the image on the xz plane or yz plane. The pixel of 255 would be represented as a scatter point in the space. In the example below, say i'm going to smash it on xz plane.

The coordinates of the scatter point depends on the row and col index of the pixel.
```shell  
    ^ col index = 2
    |
0 0 0
0 0 255 --> row index = 1
0 0 0
```  
The coordinates of the point will be (2, 0, 1), <=> (col_index, 0, row_index).  
(it's normal to have 0 at Y axis since it's on xz plane.)  

A bit more detail:  
For some unknow reason, i found that i need to filp the input image vertically.

The output of this is step is a set of scatter points, they are represented by three numpy arrays: xs, ys, zs. The following example helps you understand:  
- i have three points: 
  ```shell
  (2, 0, 1)
  (7, 0, 9)
  (6, 0, 8)
   |  |  ^--- z axis
   |  ^------ y axis
   ^--------- x axis
  ```
  Then the three numpy arrays will be:
  - xs: (2, 7, 6)
  - ys: (0, 0, 0)
  - zs: (1, 9, 8)

### Architecture - data processing


