# Installing Packages

All the packages required for the script can be installed by running the following command:
`pip install -r requirements.txt`

# Running the Script

`barcode.py` reads in an image and decodes all the barcodes, QR codes and data matrix codes within. 
Run `python barcode.py -i image.png` to find barcodes.
Results will be printed in the following format:
`[INFO] Found (type) barcode: (value)`