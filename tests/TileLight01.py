from PIL import Image, ImageFont, ImageDraw
import numpy
from blend_modes import darken_only
from blend_modes import lighten_only

T_image = Image.open('PyGame\\I_Image_01.png').resize((256, 256))
TR_image = Image.open('PyGame\\Corner.png').resize((256, 256))

imagesADI = {}

# utilities


def return_array(image):
    array = numpy.array(image)
    array = array.astype(float)
    return array


def return_darken(image_float01, image_float02):
    opacity = 1.0
    blended_img_float = darken_only(image_float01, image_float02, opacity)
    blended_img = numpy.uint8(blended_img_float)
    blended_img_raw = Image.fromarray(blended_img)
    return blended_img_raw


def return_imageText(image, text):
    imageDraw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial', 20)
    imageDraw.text((5, 5), text, font=font, fill=(128, 128, 128))
    return image

# main


# def return_lighting_tile(T_image, TR_image, neighbour):
#     if neighbour == "T":
#         res = return_imageText(T_image.rotate(0), neighbour)
#         return res
#     if neighbour == "R":
#         res = return_imageText(T_image.rotate(-90), neighbour)
#         return res
#     if neighbour == "B":
#         res = return_imageText(T_image.rotate(180), neighbour)
#         return res
#     if neighbour == "L":
#         res = return_imageText(T_image.rotate(90), neighbour)
#         return res
#     if neighbour == "TR":
#         res = return_imageText(TR_image.rotate(0), neighbour)
#         return res
#     if neighbour == "BR":
#         res = return_imageText(TR_image.rotate(-90), neighbour)
#         return res
#     if neighbour == "BL":
#         res = return_imageText(TR_image.rotate(180), neighbour)
#         return res
#     if neighbour == "TL":
#         res = return_imageText(TR_image.rotate(90), neighbour)
#         return res

# def return_blended(neighbours, debug):
#     forgound_image = neighbours.pop()
#     background_image = neighbours.pop(-1)
#     forground_array = return_array(forgound_image)
#     background_array = return_array(background_image)
#     res = return_darken(forground_array, background_array)
#     if debug == True:
#         forgound_image.show()
#         background_image.show()
#     return res

# print("imagesADI: ", type(imagesADI))
# print(imagesADI)
# print("imagesADI_123: ", imagesADI.get("T_image"))

# for key, value in imagesADI.items() :
#     print (key, type(value))
#     value.show()

# imagesADI[T_image].show()

# T_image = return_lighting_tile02(T_image, TR_image, "T")
# R_image = return_lighting_tile02(T_image, TR_image, "R")
# B_image = return_lighting_tile02(T_image, TR_image, "B")
# L_image = return_lighting_tile02(T_image, TR_image, "L")
# TR_image = return_lighting_tile02(T_image, TR_image, "TR")
# BR_image = return_lighting_tile02(T_image, TR_image, "BR")
# BL_image = return_lighting_tile02(T_image, TR_image, "BL")
# TR_image = return_lighting_tile02(T_image, TR_image, "TL")

def return_lighting_tile02(TOP_image, TOPR_image, neighbour):
    if neighbour == "T" or neighbour == "TR":
        rot = 0
    elif neighbour == "L" or neighbour == "TL":
        rot = 90
    elif neighbour == "B" or neighbour == "BL":
        rot = 180
    elif neighbour == "R" or neighbour == "BR":
        rot = 270
    if len(neighbour) == 1:
        res = TOP_image.rotate(rot)
    elif len(neighbour) == 2:
        res = TOPR_image.rotate(rot)
    # res = return_imageText(res, neighbour)
    # res.show()
    return res


def return_blended(neighbours01, neighbours02, debug):
    forgound_image = neighbours01
    background_image = neighbours02
    forground_array = return_array(forgound_image)
    background_array = return_array(background_image)
    res = return_darken(forground_array, background_array)
    if debug == True:
        forgound_image.show()
        background_image.show()
    return res


def set_images():
    image_types = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]
    for i in image_types:
        imagesADI[i + "_image"] = return_lighting_tile02(T_image, TR_image, i)


set_images()


blended_image = return_blended(
    imagesADI["B_image"], imagesADI["L_image"], False)
blended_image.show()
