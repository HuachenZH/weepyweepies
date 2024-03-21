import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista
import cv2
from tqdm import tqdm

from image_to_array import img2arr
from tamaki_iroha import scale_down
from tamaki_iroha import doppel

import pdb



def chaos_maximal(df1:pd.DataFrame, df2:pd.DataFrame) -> pd.DataFrame:
    """Chaos style, maximal points in the space.
 
            Parameters:
                    df1 (pd.DataFrame): dataframe of img on xz plane.
                    Contains two columns: "xs" and "zs". As Y axis is zero, it's omitted.

                    df2 (pd.DataFrame): dataframe of img on yz plane.
                    Contains two columns: "ys" and "zs". As X axis is zero, it's omitted.
 
            Returns:
                    df_f_chaos (pd.DataFrame): dataframe of two images combined in 3D.
    """
    df_f_chaos = pd.DataFrame({"xs":[], "ys":[], "zs":[]}, dtype=int)
    for z in set(df1["zs"].to_list() + df2["zs"].to_list()): # all z value
        df1_truncated = df1.loc[df1["zs"]==z].copy(deep=True)
        df2_truncated = df2.loc[df2["zs"]==z].copy(deep=True)
        # If one of the two is empty. Notice that it's impossible that both are empty.
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
        if df1_truncated.shape[0] < df2_truncated.shape[0]:
            df_small = df1_truncated
            df_big = df2_truncated
            col_to_fill = "xs"
            minValue = df1["xs"].min()
            maxValue = df1["xs"].max()
            size = df2_truncated.shape[0] - df1_truncated.shape[0]
        else:
            df_small = df2_truncated
            df_big = df1_truncated
            col_to_fill = "ys"
            minValue = df2["ys"].min()
            maxValue = df2["ys"].max()
            size = df1_truncated.shape[0] - df2_truncated.shape[0]
        arr_new_col = np.concatenate((df_small[col_to_fill].to_numpy(), np.random.randint(minValue, maxValue, size=size)))
        df_big.loc[:,col_to_fill] = arr_new_col
        df_f_chaos = pd.concat([df_f_chaos, df_big])
    return df_f_chaos



def chaos_minimal(df1:pd.DataFrame, df2:pd.DataFrame) -> pd.DataFrame:
    """Chaos style, minimal points in the space.
 
            Parameters:
                    df1 (pd.DataFrame): dataframe of img on xz plane.
                    Contains two columns: "xs" and "zs". As Y axis is zero, it's omitted.

                    df2 (pd.DataFrame): dataframe of img on yz plane.
                    Contains two columns: "ys" and "zs". As X axis is zero, it's omitted.
 
            Returns:
                    df_f_chaos (pd.DataFrame): dataframe of two images combined in 3D.
    """
    df_f_chaos = pd.DataFrame({"xs":[], "ys":[], "zs":[]}, dtype=int)
    for z in set(df1["zs"].to_list() + df2["zs"].to_list()): # all z value
        df1_truncated = df1.loc[df1["zs"]==z].copy(deep=True)
        df2_truncated = df2.loc[df2["zs"]==z].copy(deep=True)
        # If one of the two is empty. Notice that it's impossible that both are empty.
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
        if df1_truncated.shape[0] < df2_truncated.shape[0]:
            minValue = df1["xs"].min()
            maxValue = df1["xs"].max()
            size = df2_truncated.shape[0] - df1_truncated.shape[0]
            arr_new_col = np.concatenate((df1_truncated["xs"].to_numpy(), np.random.randint(minValue, maxValue, size=size)))
            df2_truncated.loc[:,"xs"] = arr_new_col
            df_f_chaos = pd.concat([df_f_chaos, df2_truncated])
        else:
            size_diff = df1_truncated.shape[0] - df2_truncated.shape[0]
            arr_new_col = df1_truncated["xs"].to_numpy()[0: len(df1_truncated.index)-size_diff]
            df2_truncated.loc[:,"xs"] = arr_new_col
            df_f_chaos = pd.concat([df_f_chaos, df2_truncated])
    return df_f_chaos



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



def edge():
    # Create array from image
    #path_img = "../data/txt_a2.jpg"
    path_img = "../data/txt_anae.jpg"
    xs_img1, ys_img1, zs_img1 = img2arr(path_img, False, "xz")
    #path_img = "../data/txt_q2.jpg"
    path_img = "../data/txt_quentin.jpg"
    xs_img2, ys_img2, zs_img2 = img2arr(path_img, True, "yz")

    # Create df from array
    # By convention, df2 has more rows than df1
    if len(xs_img2) > len(xs_img1):
        df1 = pd.DataFrame({"xs":xs_img1, "ys":ys_img1, "zs":zs_img1})
        df2 = pd.DataFrame({"xs":xs_img2, "ys":ys_img2, "zs":zs_img2})
    else:
        df2 = pd.DataFrame({"xs":xs_img1, "ys":ys_img1, "zs":zs_img1})
        df1 = pd.DataFrame({"xs":xs_img2, "ys":ys_img2, "zs":zs_img2})
    # Drop 0 axis
    df1 = df1[["xs", "zs"]]
    df2 = df2[["ys", "zs"]]

    # Style: Chaos middle
    df_f_chaos = chaos_middle(df1, df2)
    #__fig = plt.figure()
    #__ax = fig.add_subplot(projection='3d')
    #__ax.scatter(df_f_chaos["xs"], df_f_chaos["ys"], df_f_chaos["zs"], marker=".")
    #__ax.set_xlabel('X Label')
    #__ax.set_ylabel('Y Label')
    #__ax.set_zlabel('Z Label')
    #__fig.suptitle('Chaos middle', fontsize=16)
    #__plt.show()
    arr_f_chaos = df_f_chaos.copy(deep=True).to_numpy().astype(float)
    arr_f_chaos_scaled = (arr_f_chaos - arr_f_chaos.min())/arr_f_chaos.max()
    pdata = pyvista.PolyData(arr_f_chaos_scaled)
    pdata['orig_sphere'] = np.arange(arr_f_chaos.shape[0])
    # create many spheres from the point cloud
    sphere = pyvista.Sphere(radius=0.005, phi_resolution=10, theta_resolution=10)
    pc = pdata.glyph(scale=False, geom=sphere, orient=False)
    pc.plot(cmap='Reds')
    breakpoint()

    # Style: Chaos minimal
    df_f_chaos = chaos_minimal(df1, df2)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df_f_chaos["xs"], df_f_chaos["ys"], df_f_chaos["zs"], marker=".")
    plt.show()
    breakpoint()

    # Style: Chaos maximal
    df_f_chaos = chaos_maximal(df1, df2)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df_f_chaos["xs"], df_f_chaos["ys"], df_f_chaos["zs"], marker=".")
    plt.show()
    breakpoint()


    # Style: Order
    df_f = pd.merge(df2, df1, on="zs", how="inner")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df_f["xs"], df_f["ys"], df_f["zs"], marker=".")
    plt.show()

    #df1[df1["zs"].isin( set(df1["zs"].to_list() + df2["zs"].to_list()) )]
    breakpoint()

    #cv2.destroyAllWindows() 



def doppelize():
    # Create array from image
    #path_img1 = "../data/anae_small.jfif"
    path_img1 = "../data/anae_mid.jfif"
    #path_img2 = "../data/quentin_small.jpg"
    path_img2 = "../data/quentin_mid.jpg"

    arr_img1 = cv2.imread(path_img1, flags=0)  
    arr_img1 = cv2.flip(arr_img1, 0)
    arr_img1 = scale_down(arr_img1)
    arr_res1 = doppel(arr_img1)

    arr_img2 = cv2.imread(path_img2, flags=0)  
    arr_img2 = cv2.flip(arr_img2, 0)
    arr_img2 = scale_down(arr_img2)
    arr_res2 = doppel(arr_img2)

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
    #plotter.show()

    plotter.open_gif("../data/point_cloud.gif")
    plotter.write_frame()
    for angle_deg in tqdm(np.linspace(0, 180, 100)[:-1]):
        pdata.rotate_z(angle_deg, point=(max(arr_f_chaos[:, 0])/2, max(arr_f_chaos[:, 1])/2, max(arr_f_chaos[:, 2])/2), inplace=True)
        plotter.write_frame()
    plotter.close()




if __name__ == "__main__":
    #edge()
    doppelize()
