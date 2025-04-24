"""rmbrdr - Remove Border

Remove the border of white lines from an image.
Used as a last step after scanning a lot of photos.

Date: 20250420
Author: Rob Prikanowski
"""

import numpy as np
import cv2 as cv
import os.path

from pathlib import Path

# configuration section
directory_in_str = "C:/Users/xxx/Dropbox/foto_scans"            # directoy where the images are, no ending slash
directory_out_str = "C:/Users/xxx/Dropbox/foto_scans_cropped"   # directory to write the cropped images to, no ending slash
threshold = 254                         # threshold for white line/column
margin = 5                              # extra pixels to remove
# end of configuration section

if __name__ == '__main__':
    # print(np.__version__)
    # print(cv.__version__)

    pathlist = Path(directory_in_str).rglob('*.jpg')
    for path in pathlist:
        path_in_str = str(path)   # because path is object not string
        print(path_in_str + " --> ", end='')

        # load the image from disk and then grab the dimensions
        image = cv.imread(path_in_str)
        (h, w) = image.shape[:2]

        # display the image width, height, and number of channels to our
        # terminal
        # print("width: {} pixels".format(w))
        # print("height: {}  pixels".format(h))

        # count white lines from the top
        y = 0
        m = 255   # to satisfy the first iteration of the loop
        while (y < h - 1) and (m > threshold):
            line = image[y:y+1, 0:w]
            m = np.mean(line)
            # print("xxx = {}".format(m))
            y = y + 1
        y_top = y - 1
        # print("y_top = {}".format(y_top))

        # count white lines from the bottom
        y = h - 1
        m = 255   # to satisfy the first iteration of the loop
        while (y > 0) and (m > threshold):
            line = image[y:y+1, 0:w]
            m = np.mean(line)
            # print("xxx = {}".format(m))
            y = y - 1
        y_bottom = y + 1
        # print("y_bottom = {}".format(y_bottom))

        # count white lines from the left
        x = 0
        m = 255   # to satisfy the first iteration of the loop
        while (x < w - 1) and (m > threshold):
            col = image[0:h, x:x+1]
            m = np.mean(col)
            # print("yyy = {}".format(m))
            x = x + 1
        x_left = x - 1
        # print("x_left = {}".format(x_left))

        # count white lines from the left
        x = w - 1
        m = 255   # to satisfy the first iteration of the loop
        while (x > 0) and (m > threshold):
            col = image[0:h, x:x+1]
            m = np.mean(col)
            # print("yyy = {}".format(m))
            x = x - 1
        x_right = x + 1
        # print("x_left = {}".format(x_right))

        # get cropped image
        cropped_image = image[y_top+margin:y_bottom-margin, x_left+margin:x_right-margin]

        # determine output filename and write modified image to file
        index = len(directory_in_str)
        out_file = directory_out_str + path_in_str[index:]
        print(out_file)
        dir_path = Path(os.path.dirname(out_file))
        dir_path.mkdir(parents=True, exist_ok=True)   # create directories if they don't exist
        cv.imwrite(out_file, cropped_image)
