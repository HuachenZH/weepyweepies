import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import cv2

from image_to_array import img2arr

import pdb



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
    df_f = pd.merge(df2, df1, on="zs", how="inner")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df_f["xs"], df_f["ys"], df_f["zs"], marker=".")
    plt.show()

    # df1[df1["zs"].isin( set(df1["zs"].to_list() + df2["zs"].to_list()) )]
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

