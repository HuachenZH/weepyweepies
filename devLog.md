# DevLog

## Info
- [edge detection using opencv](https://learnopencv.com/edge-detection-using-opencv/)
- [a library called scikit-image](https://scikit-image.org/)
- you might need a stronger 3D visualization library other than matplotlib: 
  - [Pyvista, trimesh, vedo](https://towardsdatascience.com/python-libraries-for-mesh-and-point-cloud-visualization-part-1-daa2af36de30)
  - [pyviz](https://pyviz.org/scivis/index.html)

## WBS
- ~~a very basic 3d scatter plot~~
- plot portrait in one plane
  - __solution 1: use edge detection__
    - to test before edge detection: gauss blur
    - ~~image sharpening ~~
    - dichotomie
  - try to project on the plane
    - get the matrix of edge
    - extract scatter points
  - __solution 2: more points for darker pixel, less points for lighter pixel__
- plot portrait in second plane
- merge two protraits


## Encountered
- pyvista does not show anything  
  - root cause is the range of array. I scale it to 0~1 then it works


## To improve / future work
- the dictionary of doppel, more levels, more accurate presentation
- code structure
- use tqdm
- optimize memory usage
- output gif
- point size scale: bigger the closer
- image pre processing, higher contrast



to resume: 
try to make the plot more beautiful. After that, i will restart image processing
