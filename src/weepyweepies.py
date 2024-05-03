import argparse
from point_cloud import point_cloud



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--doppelSize", help="Doppel size", choices=[3,5])
    parser.add_argument("-i1", "--inputImage1", help="Input image 1, will be on xz plane", type=str)
    parser.add_argument("-i2", "--inputImage2", help="Input image 2, will be on yz plane", type=str)
    parser.add_argument("-o", "--outputPath", help="Path to the output image", type=str)
    parser.add_argument("-a", "--angleDegree", help="Angle of rotation in degree", type=float, default=2)
    parser.add_argument("-f", "--fps", help="Frame per second", type=int, default=30)
    parser.add_argument("-r", "--rotationStyle", help="Rotatioin style", choices=["360","90"], default="360")
    args = parser.parse_args()
    return args



def main():
    args = get_args()
    point_cloud(args.inputImage1, args.inputImage2, args.outputPath, args.doppelSize, args.angleDegree, args.fps, args.rotationStyle)


# python3 weepyweepies.py -d 5 -i1 ../data/img1.jpg -i2 ../data/img2.jpg -o ../data/output.gif -a 2 -f 30

if __name__ == "_main__":
    main()
