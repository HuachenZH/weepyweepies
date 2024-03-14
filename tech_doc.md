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

The output of this step is the three numpy arrays: xs, ys and zs for each input image..

For the moment, this part of code is hosted in `image_to_array.py` 


### Architecture - data processing
This step creates a point cloud in 3D, the point cloud merge the two input 2D image.  

Say that the input image1 is an image of the letter "A", the input image2 is an image of the letter "B". To be convenient, the two images have the same width and height.  

The objective is that, after plotting the point cloud in the space, if i inspect it on xz plane, i will see "A". If i inspect it on yz plane, i will see "B".  


I found two ways to do so:  
1. "standard" with pandas's merge.
2. "custom", construct the df myself.  

Let's take a look in details. As a reminder, at the end of the previous step, i got six np arrays:
- image 1: xs, ys, zs
- image 2: xs, ys, zs  

So we can get two dataframes:  
__df1__: (as it's on xz plane, Y axis is 0)  
| xs | ys | zs |
| -- | -- | -- |
| 10 | 0  | 0  |
| 13 | 0  | 0  |
| 14 | 0  | 0  |
| 11 | 0  | 1  |
| 12 | 0  | 2  |

and __df2__: (as it's on xs plane, X axis is 0)  
| xs | ys | zs |
| -- | -- | -- |
| 0  | 10 | 0  |
| 0  | 12 | 0  |
| 0  | 11 | 1  |

__The standard way__:
Use merge function of pandas.  
First drop the 0 column of each dataframe, then  
```python
df_final = pd.merge(df2, df1, on="zs", how="inner")
```
This works well, but there will be too much points.

__The custom way__:  
I want to have less points than pandas's merge. To do so,  
- iterate through each value of zs. For instance, zs = 0, i got:  
  __"df1[df1['zs']==0]"__:  
  | xs | ys | zs |
  | -- | -- | -- |
  | 10 | 0  | 0  |
  | 13 | 0  | 0  |
  | 14 | 0  | 0  |

  and __"df2[df2['zs']==0]"__:  
  | xs | ys | zs |
  | -- | -- | -- |
  | 0  | 10 | 0  |
  | 0  | 12 | 0  |
- construct a new df that contains all the minimum necessary information on xs and ys
  - in this iteration, df1 has more value on zs=0, so i take df1 as the base
  - i will keep the value of xs and zs unchanged and i will affect new values for ys
  - the new ys values are from df2. In the example, df2 has ownly two ys values, and "df1[df1['zs']==0]" has three rows
  - to fill the gap, i will repeat randomy value of ys of "df2[df2['zs']==0]" (a bit like data augmentation)
  - so the combined df will be:  

    | xs | ys | zs |
    | -- | -- | -- |
    | 10 | 10 | 0  |
    | 13 | 12 | 0  |
    | 14 | 10 (repeated) | 0  |


