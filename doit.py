import sys
import os
#import PIL.Image
from PIL import Image
from PIL.ExifTags import TAGS
from dateutil import parser

def print_usage():
    print("Usage: python doit.py <folderPath>")

def handleDateTime(fileName, dateTimeString):
    # dateTimeString is in format "YYYY:MM:DD HH:MM:SS"
    datePart = dateTimeString.split(" ")[0]
    datePart = datePart.replace(":", "-")
    # convert datePart to YYYYMMDD - later configurable
    datePart = parser.parse(datePart).strftime('%Y%m%d')
    newFileName = f"{datePart}_{fileName}"
    print(f"Renaming {fileName} to {newFileName}")
    return newFileName
    
# check for size of args and print usage if not correct
if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)
folderPath = sys.argv[1]
print(f"Folder: {folderPath}")
# check if folder exists and print usage if not correct
if (not os.path.exists(folderPath)) or (not os.path.isdir(folderPath)):
    print("Folder does not exist or is not a directory")
    print_usage()
    sys.exit(1)

# loop over all files in folder
for filename in os.listdir(folderPath):
    # try to read DateTaken from EXIF data
    try:
        imagePath = os.path.join(folderPath, filename)
        image = Image.open(imagePath)
        exifdata = image.getexif()
        dateTaken = None
        # read DateTaken from file properties
        
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            print(f"Tag: {tag}, ID: {tag_id}")
            data = exifdata.get(tag_id)
            if tag == "DateTime":
                dateTaken = data
                image.close()
                break
            image.close()
        if dateTaken:
            print(f"{filename}: Date Taken - {dateTaken}")
            newfilename = handleDateTime(filename, dateTaken)
            newfilenamepath = os.path.join(folderPath, newfilename)
            print   (f"Renaming {imagePath} to {newfilenamepath}")
            os.rename(imagePath, os.path.join(folderPath, newfilename))
        else:
            print(f"{filename}: No Date Taken found in EXIF data")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

