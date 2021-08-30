# import the necessary packages
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx
import argparse
import numpy as np
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

# GPU
# gpu_frame = cv2.cuda_GpuMat()
# gpu_frame.upload(image)

# image = cv2.resize(image, (240, 160))
# min resolution for the barcode to be recognized: 400 * 320
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cols, rows = image.shape
brightness = np.sum(image) / (255.0 * cols * rows)
minimum_brightness = 0.66
ratio = brightness / minimum_brightness
print(ratio)
if ratio < 1:
    image = cv2.convertScaleAbs(image, alpha = 1 / ratio, beta = 0)

# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)

if len(barcodes) == 0:
    print("nope")
    dmc = pylibdmtx.decode(image)
    if len(dmc) == 0:
        print("No Barcodes Found!")
    else:
        # loop over the detected barcodes
        for code in dmc:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image
            (x, y, w, h) = code.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = code.data.decode("utf-8")
            barcodeType = "Data Matrix Code"
            # print the barcode type and data to the terminal
            print("[INFO] Found {} DMC: {}".format(barcodeType, barcodeData))
else:
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# image = image.download()
cv2.imshow("Image", image)
cv2.waitKey(0)

# resolution threshold
# flat field correction
