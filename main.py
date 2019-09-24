import glob
import cv2
import numpy as np
import argparse
from skimage import data

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    

def define_rect(image):
    """
    Define a rectangular window by click and drag your mouse.

    Parameters
    ----------
    image: Input image.
    """
    clone = image.copy()
    rect_pts = [] # Starting and ending points
    win_name = "image" # Window name

    def select_points(event, x, y, flags, param):

        nonlocal rect_pts
        if event == cv2.EVENT_LBUTTONDOWN:
            rect_pts = [(x, y)]

        if event == cv2.EVENT_LBUTTONUP:
            rect_pts.append((x, y))

            # draw a rectangle around the region of interest
            cv2.rectangle(clone, rect_pts[0], rect_pts[1], (0, 255, 0), 2)
            cv2.imshow(win_name, clone)
    ##ADD CONDITION TO CHECK IF THE DRAWN RECT IS CORRECT
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, select_points)

    while True:
        # display the image and wait for a keypress
        cv2.imshow(win_name, clone)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("r"): # Hit 'r' to replot the image
            clone = image.copy()
            rect_pts = []

        elif key == ord("c"): # Hit 'c' to confirm the selection
            break

        elif key == ord("q"): # Hit 'c' to confirm the selection
            return None

    # close the open windows
    cv2.destroyWindow(win_name)

    return rect_pts


parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, default="labels.txt", help='File to save the labels')
parser.add_argument('--mode', type=str, default="append", help='Select "append", or "write" mode.')
parser.add_argument('--dir', type=str, default=None, help='Directory of images to label.')
parser.add_argument('--class_label', type=str, default=None, help='Input the name of the class in the given directory that will be labeled')
parser.add_argument('--img_format', type=str, default="jpg", help='Image format to search in the directory')
parser.add_argument('--output_schema', type=str, default="2", help='"1" = imgName, x1, y1, x2, y2, class\n"2" = imgName, width, height, class, xmin, ymin, xmax, ymax\n')


#parser.add_argument('--dataset', type=str, default="Pets", help='Dataset you are using.')
args = parser.parse_args()

imgDir = args.dir
lbl_class = args.class_label
write_mode = args.mode
file_to_save = args.file
imgformat = args.img_format
outFormat = args.output_schema

if (write_mode=="append"):
    wtype = "a"
else:
    wtype = "w"
    f = open(file_to_save, "w")
    f.close()



if (imgDir is not None and lbl_class is not None):
    print("Commands:\n'C' to confirm selection\n'R' to replot image\n'Q' to quit labelling\n")
    for imgName in glob.glob(imgDir+"/*."+imgformat):
        coords = define_rect(cv2.imread(imgName))
        #imgName, x1, y1, x2, y2, class
        if coords is not None and len(coords) > 0:
            if  outFormat == "1":
                f = open(file_to_save, "a")
                f.write(imgName.replace("\\","/") + ","+ str(coords[0][0]) + ","+ str(coords[0][1]) + ","+ str(coords[1][0]) + ","+ str(coords[1][1]) + ","+lbl_class+"\n")
                f.close()
                print (imgName + ", "+ str(coords[0][0]) + ","+ str(coords[0][1]) + ","+ str(coords[1][0]) + ","+ str(coords[1][1]) + ","+lbl_class+"\n")
            else:
                f = open(file_to_save, "a")
                f.write(imgName.replace("\\","/").split("/")[-1] + ","+ str(np.abs(coords[0][0]-coords[1][0])) + ","+ str(np.abs(coords[0][1]-coords[1][1]))+ ","+ lbl_class + ","+ str(coords[0][0]) + ","+ str(coords[0][1]) + ","+ str(coords[1][0]) + ","+str(coords[1][1])+"\n")
                f.close()
                print (imgName.replace("\\","/").split("/")[-1] + ","+ str(np.abs(coords[0][0]-coords[1][0])) + ","+ str(np.abs(coords[0][1]-coords[1][1]))+ ","+ lbl_class + ","+ str(coords[0][0]) + ","+ str(coords[0][1]) + ","+ str(coords[1][0]) + ","+str(coords[1][1])+"\n")
        elif coords is None:
            break
    print("Labelling done.")
