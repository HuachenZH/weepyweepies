import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cv2

from image_to_array import img2arr

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



def main():
    # Create array from image
    path_img = "../data/txt_a.jpg"
    xs_img1, ys_img1, zs_img1 = img2arr(path_img, False, "xz")
    path_img = "../data/txt_q.jpg"
    xs_img2, ys_img2, zs_img2 = img2arr(path_img, True, "yz")

    # Create df from array
    df1 = pd.DataFrame({"xs":xs_img1, "ys":ys_img1, "zs":zs_img1})
    df2 = pd.DataFrame({"xs":xs_img2, "ys":ys_img2, "zs":zs_img2})
    # Drop 0 axis
    df1 = df1[["xs", "zs"]]
    df2 = df2[["ys", "zs"]]
    # Style: Chaos
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

    # Prepare for plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs_img1, ys_img1, zs_img1, marker='.')
    ax.scatter(xs_img2, ys_img2, zs_img2, marker='^')
    plt.show()
    #cv2.destroyAllWindows() 



if __name__ == "__main__":
    main()

