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
import gc



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



def doppelize(path_img:str, doppel_size:int, alpha:float=1.0, beta:float=0.0) -> np.ndarray:
    """Convert magical girls to doppels. Bundle of preprocessing + doppel().
 
            Parameters:
                    path_img (str): path of input image.
 
                    doppel_size (int): one pixel will become x pixels after doppelization.
 
                    alpha (float): contrast control.
 
                    beta (float): brightness control.
 
            Returns:
                    (np.ndarray): matrix of 0 and 1. 1 represents a dark pixel.
    """
    arr_img = cv2.imread(path_img, flags=0)  
    arr_img = cv2.flip(arr_img, 0)
    arr_img = cv2.convertScaleAbs(arr_img, alpha=alpha, beta=beta)
    arr_img = scale_down(arr_img, doppel_size)
    arr_img = doppel(arr_img, doppel_size)
    return arr_img



def projection_on_plane(arr_img:np.ndarray, plane:str) -> pd.DataFrame:
    """Project the array of "doppelized" image onto a plane of a 3D space.
 
            Parameters:
                    arr_img (np.ndarray): array of "doppelized" image.

                    plane (str): project the array on which plane, xz or yz.
 
            Returns:
                    df_res (pd.DataFrame): dataframe of two colume:
                    - xs and zs if plane xz is chosen. ys is always 0 thus omitted.
                    - ys and zs if plane yz is chosen. xs is always 0 thus omitted.
                    Each row is the coordinates of a point.
    """
    if plane.lower() == "xz":
        zs, xs = np.where(arr_img==1)
        df_res = pd.DataFrame({"xs":xs, "zs":zs})
        return df_res
    elif plane.lower() == "yz":
        zs, ys = np.where(arr_img==1)
        df_res = pd.DataFrame({"ys":ys, "zs":zs})
        return df_res
    elif plane.lower() == "xy":
        raise ValueError("Feature not yet build")
    else:
        raise ValueError("You can only put xz, yz or xy as plane.")



def rise_chaos(arr_doppel1:np.ndarray, arr_doppel2:np.ndarray) -> np.ndarray:
    """Mix the images in 3D space.
 
            Parameters:
                    arr_doppel1 (np.ndarray): array of "doppelized" image 1.

                    arr_doppel2 (np.ndarray): array of "doppelized" image 2.
 
            Returns:
                    arr_f_chaos (np.ndarray): array of point cloud. The images are mixed,
                    all of them can be seened.
    """
    # Smash img1 on plane xz, img2 on plane yz.
    df1 = projection_on_plane(arr_doppel1, "xz")
    df2 = projection_on_plane(arr_doppel2, "yz")
    # chaos
    df_f_chaos = chaos_middle(df1, df2)
    #arr_f_chaos = df_f_chaos.copy(deep=True).to_numpy().astype(float)
    arr_f_chaos = df_f_chaos.to_numpy().astype(float)
    arr_f_chaos = (arr_f_chaos - arr_f_chaos.min())/arr_f_chaos.max()
    return arr_f_chaos



def point_cloud(path_img1:str, path_img2:str, path_out:str, doppel_size:int, angle_deg:float, fps:int, rotation_style:str):
    """Mash up two images into a point cloud, output a gif.
 
            Parameters:
                    path_img1 (str): path to input image 1.

                    path_img2 (str): path to input image 2.

                    path_out (str): path to the output gif.

                    doppel_size (int): after transform, a pixel corresponds to how many points.

                    angle_deg (float): rotate how many degrees between each frame.

                    fps (int): frame per second of gif.

                    rotation_style (str): rotation style.
 
            Returns:
                    None. Gif written to disk directly.
    """
    # Convert magical girls to doppels.
    arr_res1 = doppelize(path_img1, doppel_size, 1.5, 0)
    arr_res2 = doppelize(path_img2, doppel_size)

    # Mesh the two image, end of data processing, start of visualization
    arr_f_chaos = rise_chaos(arr_res1, arr_res2)
    pdata = pyvista.PolyData(arr_f_chaos)

    # Free some memory
    point_of_rotation_center = (max(arr_f_chaos[:, 0])/2, max(arr_f_chaos[:, 1])/2, max(arr_f_chaos[:, 2])/2)
    del arr_f_chaos
    del arr_res1
    del arr_res2
    gc.collect() # This helps avoid fragmenting memory.

    # Visualization stuffs, output to gif
    plotter = pyvista.Plotter()
    plotter.add_mesh(pdata, style="points", color='black', point_size=0.005, render_points_as_spheres=False, lighting=False)
    plotter.view_xz() # set the first view when visualization starts.
    #plotter.show_axes()
    #plotter.show()
    #_breakpoint()

    if rotation_style == "360":
        # 360°
        plotter.open_gif(path_out, fps=fps, subrectangles=True)
        plotter.write_frame() # write the first frame before rotating
        for _ in tqdm(np.linspace(0, 360, int(360/angle_deg))[:-1]):
            pdata.rotate_z(angle_deg, point=point_of_rotation_center, inplace=True)
            plotter.write_frame()
        plotter.close()

    if rotation_style == "90":
        #90° * 2
        plotter.open_gif(path_out, fps=fps, subrectangles=True)
        plotter.write_frame() # write the first frame before rotating
        for _ in tqdm(np.linspace(0, 90, int(90/angle_deg))[:-1]):
            pdata.rotate_z(-1*angle_deg, point=point_of_rotation_center, inplace=True)
            plotter.write_frame()
        for _ in tqdm(np.linspace(0, 90, int(90/angle_deg))[:-1]):
            pdata.rotate_z(angle_deg, point=point_of_rotation_center, inplace=True)
            plotter.write_frame()
        plotter.close()

    print(f"Gif written to {path_out}")


def main():
    doppel_size = 5
    path_img1 = "../data/le_r_1.jpg"
    path_img2 = "../data/le_r_2.jpg"
    path_out = "../data/point_cloud_r.gif"
    angle_deg = 1
    fps = 25
    point_cloud(path_img1, path_img2, path_out, doppel_size, angle_deg, fps)



if __name__ == "__main__":
    main()
