import numpy as np
import pyvista as pv


mesh = pv.Cube()
rot = mesh.rotate_z(30, inplace=False)

pl = pv.Plotter()
_ = pl.add_mesh(rot)
_ = pl.add_mesh(mesh, style='wireframe', line_width=3)
_ = pl.add_axes_at_origin()
pl.show()