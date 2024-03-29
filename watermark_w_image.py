from PIL import Image, ImageEnhance

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

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        #layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
        layer.paste(mark, (int((im.size[0] - w) / 2), int((im.size[1] - h) / 2)))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def test():
    im = Image.open('Matthew_profile_square.png')
    mark = Image.open('world_salsa_solo_logo_transparent.png')
    print ("im & mark loaded")
    print ("tile")
    #watermark(im, mark, 'tile', 0.5).show()
    watermark(im, mark, 'tile', 0.5).save("watermarked-1.jpg", 'JPEG')
    print ("scale")
    #watermark(im, mark, 'scale', 1.0).show()
    watermark(im, mark, 'scale', 1.0).save("watermarked-2.jpg", 'JPEG')
    print ("absolute position")
    #watermark(im, mark, (100, 100), 0.5).show()
    watermark(im, mark, (0, 0), 0.5).save("watermarked-3.jpg", 'JPEG')

if __name__ == '__main__':
    test()