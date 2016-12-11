"""
reworked by bmt for bulk event watermarking
originally from http://pythoncentral.io/watermark-images-python-2x/
also from http://code.activestate.com/recipes/362879-watermark-with-pil/

"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, sys

print ("--------")
#----------------config start-----------------------
FONT = 'arial.ttf' #standard font, should be on all windows machines
suffixFileName = "_watermarked"#.jpg added in code
waterMarkText = "facebook.com/LatinDanceVideosAu/"
watermark = "world_salsa_solo_logo_transparent_watermark.png"
opacityText = 0.25
opacityImage = 0.5
#----------------config end-------------------------

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im



def add_watermark(in_file, angle=0):
    out_file = in_file[:len(in_file)-4] + suffixFileName
    print ("out_file=", out_file)
    #print ("opening file")
    img = Image.open(in_file).convert('RGB')
    #print ("file opened")
    print ("img.size = ", img.size)
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    size = 2
    #start with small font size, then increment to fit image width.
    #print ("creating font")
    n_font = ImageFont.truetype(FONT, size)
    #print ("font created")
    n_width, n_height = n_font.getsize(waterMarkText)
    #increment font size until waterMarkText length does not exceed width of image/3.
    while (n_width + n_height < watermark.size[0]/2):
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(waterMarkText)
        print ("n_width=", n_width, ", n_height=", n_height)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    #position waterMarkText in middle of watermark image.
    """
    draw.text(((watermark.size[0] - n_width) / 2,
               (watermark.size[1] - n_height) / 2),
              waterMarkText, font=n_font)
    """
    draw.text( ((watermark.size[0] - n_width) / 2, (watermark.size[1] - n_height) ), waterMarkText, font=n_font)
    #rotate the watermark image by angle degrees
    watermark = watermark.rotate(angle, Image.BICUBIC)
    #repeat above to write filename on image at top of image
    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(in_file)
    while (n_width + n_height < watermark.size[0]/2):
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(in_file)
        #print ("n_width=", n_width, ", n_height=", n_height)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    #position text in middle & at top of watermark image.
    draw.text(((watermark.size[0] - n_width) / 2, n_height), in_file, font=n_font)

    #On the alpha channel, we reduce the opacity of the watermark
    # (eg: reduce brightness and contrast) by the default value of 0.25.
    # (Note: value 1 returns the original image).
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacityText)
    watermark.putalpha(alpha)
    #
    Image.composite(watermark, img, watermark).save(out_file+".jpg", 'JPEG')
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
    if isfile(f) and suffixFileName not in f and (".jpg" in f or ".png" in f):
        print (f)
        add_watermark(f)


#add_watermark("./Matthew_profile_square.png", "facebook.com/LatinDanceVideosAu/")
