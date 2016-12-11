"""
reworked by bmt for bulk event watermarking
originally from http://pythoncentral.io/watermark-images-python-2x/
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys

FONT = 'arial.ttf'
print ("--------")
#----------------config start-----------------------
watermarkedFileNameSuffix = "_watermarked.jpg"#must be .jpg
waterMarkText = "facebook.com/LatinDanceVideosAu/"
#----------------config end-------------------------

def add_watermark(in_file, text, out_file=watermarkedFileNameSuffix, angle=0, opacity=0.25):
    out_file = in_file[:len(in_file)-4] + out_file
    print ("out_file=", out_file)
    #print ("opening file")
    img = Image.open(in_file).convert('RGB')
    #print ("file opened")
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    size = 2
    #print ("creating font")
    n_font = ImageFont.truetype(FONT, size)
    #print ("font created")
    n_width, n_height = n_font.getsize(text)
    #increment font size until text length does not exceed width of image.
    while (n_width + n_height < watermark.size[0]):
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
        #print ("n_width=", n_width, ", n_height=", n_height)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    #position text in middle of watermark image.
    draw.text(((watermark.size[0] - n_width) / 2,
               (watermark.size[1] - n_height) / 2),
              text, font=n_font)
    #rotate the watermark image by angle degrees
    watermark = watermark.rotate(angle, Image.BICUBIC)
    #On the alpha channel, we reduce the opacity of the watermark
    # (eg: reduce brightness and contrast) by the default value of 0.25.
    # (Note: value 1 returns the original image).
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    #
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
    #print ("end of function")

"""
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s <input-image> <text> <output-image> ' \
                 '<angle> <opacity> ' % os.path.basename(sys.argv[0]))
    add_watermark(*sys.argv[1:])
"""

from os import listdir
from os.path import isfile, join
mypath = "./"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print (onlyfiles)
print (type(onlyfiles))

for f in listdir(mypath):
    if isfile(f) and watermarkedFileNameSuffix not in f and (".jpg" in f or ".png" in f):
        print (f)
        add_watermark(f, waterMarkText)

#add_watermark("./Matthew_profile_square.png", "facebook.com/LatinDanceVideosAu/")

