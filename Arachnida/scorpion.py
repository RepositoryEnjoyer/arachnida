# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cmaurici <cmaurici@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 11:41:13 by cmaurici          #+#    #+#              #
#    Updated: 2023/06/01 19:48:44 by cmaurici         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from PIL import Image
from PIL.ExifTags import TAGS
import sys
import os.path
import time

# Function to extract EXIF data from an image file

def get_exif_data(filename):
    with Image.open(filename) as img:
        exifdata = img.getexif()
        if exifdata:
            exif = {}
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                exif[tag] = value
            return exif
        else:
            return None

# getctime and getmtime gives us some extra information that getexif is not capable of getting.
# It also checks first if the path to the file exists

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    for filename in sys.argv[1:]:
        if not os.path.exists(filename):
            print("File not found: ", filename)
        else:
            print("File %s" % filename)
            exif = get_exif_data(filename)
            print("Creation time: ", time.ctime(os.path.getctime(filename)))
            print("Modification time: ", time.ctime(os.path.getmtime(filename)))
            print("Size: ", os.path.getsize(filename), "bytes")
            if exif:
                print("EXIF data: ")
                for tag, value in exif.items():
                    print("%s = %s" % (tag, value))
            else:
                print("No EXIF data found :(")         

