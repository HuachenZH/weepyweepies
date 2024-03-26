import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista
import cv2
from tqdm import tqdm

from tamaki_iroha import scale_down
from tamaki_iroha import doppel

import pdb



def chaos_middle(df1:pd.DataFrame, df2:pd.DataFrame) -> pd.DataFrame:
    """Chaos style, points in the space just in need.
 
            Parameters:
                    df1 (pd.DataFrame): dataframe of img on xz plane.
                    Contains two columns: "xs" and "zs". As Y axis is zero, it's omitted.

                    df2 (pd.DataFrame): dataframe of img on yz plane.
                    Contains two columns: "ys" and "zs". As X axis is zero, it's omitted.
 
            Returns:
                    df_f_chaos (pd.DataFrame): dataframe of two images combined in 3D.
                    Three columns: xs, ys, zs. Each row is the coordinate of a point in the space.
    """
    df_f_chaos = pd.DataFrame({"xs":[], "ys":[], "zs":[]}, dtype=int)
    for z in set(df1["zs"].to_list() + df2["zs"].to_list()): # all z values
        df1_truncated = df1.loc[df1["zs"]==z].copy(deep=True)
        df2_truncated = df2.loc[df2["zs"]==z].copy(deep=True)
        # If one of the two is empty. Notice that it's impossible that both are empty.
        # THis should not occur if the input images are carefully pruned (same height).
        if df1_truncated.empty:
            # if nothing found in df1, then take df2, affect random values and append to df chaos
            df2_truncated.loc[:,"xs"] = np.random.randint(df1["xs"].min(), df1["xs"].max(), size=df2_truncated.shape[0])
            df_f_chaos = pd.concat([df_f_chaos, df2_truncated])
            continue
        if df2_truncated.empty:
            df1_truncated.loc[:,"ys"] = np.random.randint(df2["ys"].min(), df2["ys"].max(), size=df1_truncated.shape[0])
            df_f_chaos = pd.concat([df_f_chaos, df1_truncated])
            continue
        # If none of the two is empty.
        if len(df1_truncated.index) == len(df2_truncated.index):
            df2_truncated.loc[:, "xs"] = df1_truncated.sample(frac=1).loc[:, "xs"].to_list()
            df_f_chaos = pd.concat([df_f_chaos, df2_truncated])
        # Q > A, within zs, too much ys, not enough xs
        elif len(df1_truncated.index) < len(df2_truncated.index):
            int_diff = len(df2_truncated.index) - len(df1_truncated.index)
            # randomly take the value of xs and repeat n times.
            list_xs = [random.choice(df1_truncated["xs"].to_list()) for i in range(int_diff)] + df1_truncated["xs"].to_list()
            random.shuffle(list_xs)
            df2_truncated.loc[:, "xs"] = list_xs
            df_f_chaos = pd.concat([df_f_chaos, df2_truncated])
        # Q < A, within zs, too much xs, not enough ys
        else:
            int_diff = len(df1_truncated.index) - len(df2_truncated.index)
            # randomly take the value of ys and repeat n times 
            list_ys = [random.choice(df2_truncated["ys"].to_list()) for i in range(int_diff)] + df2_truncated["ys"].to_list()
            random.shuffle(list_ys)
            df1_truncated.loc[:, "ys"] = list_ys
            df_f_chaos = pd.concat([df_f_chaos, df1_truncated])
    return df_f_chaos



def doppelize(path_img:str) -> np.ndarray:
    arr_img = cv2.imread(path_img, flags=0)  
    arr_img = cv2.flip(arr_img, 0)
    arr_img = scale_down(arr_img)
    return doppel(arr_img)


def main():
    # convert magical girls to doppels
    arr_res1 = doppelize("../data/anae_mid.jfif")
    arr_res2 = doppelize("../data/quentin_mid.jpg")


    zs, xs = np.where(arr_res1==1)
    df1 = pd.DataFrame({"xs":xs, "zs":zs})
    zs, ys = np.where(arr_res2==1)
    df2 = pd.DataFrame({"ys":ys, "zs":zs})

    df_f_chaos = chaos_middle(df1, df2)
    arr_f_chaos = df_f_chaos.copy(deep=True).to_numpy().astype(float)
    arr_f_chaos = (arr_f_chaos - arr_f_chaos.min())/arr_f_chaos.max()
    pdata = pyvista.PolyData(arr_f_chaos)

    #__#pdata['orig_sphere'] = np.arange(arr_f_chaos.shape[0])
    #__# create many spheres from the point cloud
    #__sphere = pyvista.Sphere(radius=0.0008, phi_resolution=10, theta_resolution=10)
    #__pc = pdata.glyph(scale=False, geom=sphere, orient=False)
    #__#pc.plot(cmap='Reds')
    #__pc.plot()

    plotter = pyvista.Plotter()
    plotter.add_mesh(pdata, style="points", color='maroon', point_size=0.005, render_points_as_spheres=False, lighting=False)
    plotter.view_xz()
    #plotter.show_axes()
    plotter.show()

    #--plotter.open_gif("../data/point_cloud.gif", fps=40, subrectangles=True)
    #--plotter.write_frame()
    #--angle_deg = 1
    #--for _ in tqdm(np.linspace(0, 360, int(360/angle_deg))[:-1]):
    #--    pdata.rotate_z(angle_deg, point=(max(arr_f_chaos[:, 0])/2, max(arr_f_chaos[:, 1])/2, max(arr_f_chaos[:, 2])/2), inplace=True)
    #--    plotter.write_frame()
    #--plotter.close()



if __name__ == "__main__":
    main()
