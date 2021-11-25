from PIL import Image, ImageFont, ImageDraw
import numpy
from blend_modes import darken_only

ADITESTDICT = {(0, 96): ['TR'],
             (0, 128): ['R', 'TR'],
             (0, 160): ['BR', 'R', 'TR'],
             (0, 192): ['BR', 'R', 'TR'],
             (0, 224): ['BR', 'R', 'TR'],
             (0, 256): ['BR', 'R', 'TR'],
             (0, 288): ['BR', 'R', 'TR'],
             (0, 320): ['BR', 'R', 'TR'],
             (0, 352): ['BR', 'R'],
             (0, 384): ['BR'],
             (0, 448): ['TR'],
             (0, 480): ['R'],
             (0, 512): ['BR'],
             (32, 96): ['T'],
             (32, 384): ['B'],
             (32, 448): ['T', 'TR'],
             (32, 512): ['B', 'BR'],
             (64, 96): ['TL'],
             (64, 128): ['L', 'TL'],
             (64, 160): ['BL', 'L', 'TL'],
             (64, 192): ['BL', 'L', 'TL'],
             (64, 224): ['BL', 'L', 'TL'],
             (64, 256): ['BL', 'L', 'TL', 'T', 'TR'],
             (64, 320): ['BL', 'L', 'TL', 'B', 'BR', 'R', 'TR'],
             (64, 352): ['BL', 'L', 'BR', 'R', 'TR'],
             (64, 384): ['BL', 'BR', 'R', 'TR'],
             (64, 416): ['BR', 'R', 'TR'],
             (64, 448): ['TL', 'T', 'BR', 'R', 'TR'],
             (64, 512): ['BL', 'B', 'BR', 'R', 'TR'],
             (64, 544): ['BR', 'R'],
             (64, 576): ['BR'],
             (96, 256): ['TL', 'T', 'TR'],
             (96, 576): ['B'],
             (128, 192): ['TR'],
             (128, 224): ['R', 'TR'],
             (128, 256): ['TL', 'T', 'BR', 'R', 'TR'],
             (128, 320): ['BL', 'L', 'TL', 'B', 'BR', 'TR'],
             (128, 352): ['BL', 'L', 'TL', 'R', 'TR'],
             (128, 384): ['BL', 'L', 'TL', 'BR', 'R', 'TR'],
             (128, 416): ['BL', 'L', 'TL', 'BR', 'R', 'TR'],
             (128, 448): ['BL', 'L', 'TL', 'T', 'BR', 'R', 'TR'],
             (128, 512): ['BL', 'L', 'TL', 'B', 'BR'],
             (128, 544): ['BL', 'L'],
             (128, 576): ['BL'],
             (160, 192): ['T'],
             (160, 320): ['BL', 'B', 'T', 'BR', 'TR'],
             (160, 512): ['BL', 'B', 'BR'],
             (192, 192): ['TL'],
             (192, 224): ['L', 'TL'],
             (192, 256): ['BL', 'L', 'TL', 'T', 'TR'],
             (192, 320): ['BL', 'TL', 'B', 'T', 'BR', 'TR'],
             (192, 384): ['BL', 'L', 'TL', 'B', 'BR'],
             (192, 416): ['BL', 'L', 'TL'],
             (192, 448): ['BL', 'L', 'TL', 'T', 'TR'],
             (192, 512): ['BL', 'B', 'BR', 'TR'],
             (192, 544): ['R', 'TR'],
             (192, 576): ['BR', 'R', 'TR'],
             (192, 608): ['BR', 'R'],
             (192, 640): ['BR'],
             (224, 256): ['TL', 'T'],
             (224, 320): ['BL', 'TL', 'B', 'T', 'TR'],
             (224, 384): ['BL', 'B', 'BR'],
             (224, 448): ['TL', 'T', 'TR'],
             (224, 512): ['BL', 'B', 'T', 'BR', 'TR'],
             (224, 640): ['B', 'BR'],
             (256, 256): ['TL'],
             (256, 288): ['L'],
             (256, 320): ['BL', 'TL', 'T', 'TR'],
             (256, 384): ['BL', 'B', 'BR'],
             (256, 448): ['TL', 'T', 'TR'],
             (256, 512): ['BL', 'TL', 'B', 'T', 'BR', 'R', 'TR'],
             (256, 576): ['BL', 'L', 'TL', 'B', 'T', 'BR', 'TR'],
             (256, 640): ['BL', 'B', 'BR', 'R', 'TR'],
             (256, 672): ['BR', 'R'],
             (256, 704): ['BR'],
             (288, 320): ['TL', 'T', 'TR'],
             (288, 384): ['BL', 'B', 'BR'],
             (288, 448): ['TL', 'T', 'TR'],
             (288, 576): ['BL', 'TL', 'B', 'T'],
             (288, 704): ['B', 'BR'],
             (320, 320): ['TL', 'T', 'TR'],
             (320, 384): ['BL', 'B', 'BR', 'R', 'TR'],
             (320, 416): ['BR', 'R'],
             (320, 448): ['TL', 'T', 'BR', 'TR'],
             (320, 512): ['BL', 'L', 'TL', 'B', 'BR'],
             (320, 544): ['BL', 'L'],
             (320, 576): ['BL', 'TL'],
             (320, 608): ['L', 'TL'],
             (320, 640): ['BL', 'L', 'TL', 'T', 'TR'],
             (320, 704): ['BL', 'B', 'BR'],
             (352, 320): ['TL', 'T'],
             (352, 448): ['TL', 'B', 'T', 'BR', 'TR'],
             (352, 512): ['BL', 'B', 'BR'],
             (352, 640): ['TL', 'T', 'TR'],
             (352, 704): ['BL', 'B', 'BR'],
             (384, 256): ['TR'],
             (384, 288): ['R'],
             (384, 320): ['TL', 'BR'],
             (384, 352): ['L', 'TL'],
             (384, 384): ['BL', 'L', 'TL', 'T', 'TR'],
             (384, 448): ['BL', 'TL', 'B', 'T', 'BR', 'TR'],
             (384, 512): ['BL', 'B', 'BR', 'R', 'TR'],
             (384, 544): ['BR', 'R'],
             (384, 576): ['BR'],
             (384, 640): ['TL', 'T', 'TR'],
             (384, 704): ['BL', 'B', 'BR'],
             (416, 256): ['T', 'TR'],
             (416, 320): ['B', 'BR'],
             (416, 384): ['TL', 'T', 'TR'],
             (416, 448): ['BL', 'TL', 'B', 'T', 'BR'],
             (416, 576): ['B', 'BR'],
             (416, 640): ['TL', 'T'],
             (416, 704): ['BL', 'B'],
             (448, 192): ['TR'],
             (448, 224): ['R', 'TR'],
             (448, 256): ['TL', 'T', 'BR', 'R', 'TR'],
             (448, 320): ['BL', 'B', 'BR', 'R', 'TR'],
             (448, 352): ['BR', 'R', 'TR'],
             (448, 384): ['TL', 'T', 'BR', 'R', 'TR'],
             (448, 448): ['BL', 'TL', 'B', 'BR'],
             (448, 480): ['L', 'TL'],
             (448, 512): ['BL', 'L', 'TL', 'T', 'TR'],
             (448, 576): ['BL', 'B', 'BR', 'R', 'TR'],
             (448, 608): ['BR', 'R'],
             (448, 640): ['TL', 'BR'],
             (448, 672): ['L'],
             (448, 704): ['BL'],
             (480, 192): ['T', 'TR'],
             (480, 448): ['BL', 'B'],
             (480, 512): ['TL', 'T'],
             (480, 640): ['B', 'BR'],
             (512, 128): ['TR'],
             (512, 160): ['R', 'TR'],
             (512, 192): ['TL', 'T', 'BR', 'R', 'TR'],
             (512, 256): ['BL', 'L', 'TL', 'B', 'BR', 'TR'],
             (512, 288): ['BL', 'L', 'TL', 'R', 'TR'],
             (512, 320): ['BL', 'L', 'TL', 'T', 'BR', 'R', 'TR'],
             (512, 384): ['BL', 'L', 'TL', 'B', 'BR', 'TR'],
             (512, 416): ['BL', 'L', 'R', 'TR'],
             (512, 448): ['BL', 'BR', 'R', 'TR'],
             (512, 480): ['BR', 'R'],
             (512, 512): ['TL', 'BR'],
             (512, 544): ['L', 'TL'],
             (512, 576): ['BL', 'L', 'TL', 'T', 'TR'],
             (512, 640): ['BL', 'B', 'BR', 'R', 'TR'],
             (512, 672): ['BR', 'R'],
             (512, 704): ['BR'],
             (544, 128): ['T'],
             (544, 256): ['BL', 'B', 'T', 'TR'],
             (544, 384): ['BL', 'B', 'T'],
             (544, 512): ['B', 'BR'],
             (544, 576): ['TL', 'T'],
             (544, 704): ['B', 'BR'],
             (576, 128): ['TL'],
             (576, 160): ['L', 'TL'],
             (576, 192): ['BL', 'L', 'TL'],
             (576, 224): ['BL', 'L'],
             (576, 256): ['BL', 'TL', 'T', 'TR'],
             (576, 320): ['BL', 'L', 'TL', 'B', 'BR'],
             (576, 352): ['BL', 'L'],
             (576, 384): ['BL', 'TL', 'TR'],
             (576, 416): ['L', 'TL', 'R', 'TR'],
             (576, 448): ['BL', 'L', 'TL', 'T', 'BR', 'R', 'TR'],
             (576, 512): ['BL', 'B', 'BR', 'TR'],
             (576, 544): ['R', 'TR'],
             (576, 576): ['TL', 'BR', 'R', 'TR'],
             (576, 608): ['L', 'TL', 'BR', 'R'],
             (576, 640): ['BL', 'L', 'TL', 'T', 'BR', 'TR'],
             (576, 704): ['BL', 'B', 'BR'],
             (608, 256): ['TL', 'T', 'TR'],
             (608, 320): ['BL', 'B', 'BR'],
             (608, 384): ['T', 'TR'],
             (608, 512): ['BL', 'B', 'T', 'BR', 'TR'],
             (608, 640): ['TL', 'B', 'T', 'TR'],
             (608, 704): ['BL', 'B', 'BR'],
             (640, 192): ['TR'],
             (640, 224): ['R', 'TR'],
             (640, 256): ['TL', 'T', 'BR', 'R', 'TR'],
             (640, 320): ['BL', 'B', 'BR'],
             (640, 384): ['TL', 'T', 'TR'],
             (640, 448): ['BL', 'L', 'TL', 'B', 'T', 'BR', 'TR'],
             (640, 512): ['BL', 'TL', 'B', 'T', 'BR', 'R', 'TR'],
             (640, 576): ['BL', 'L', 'TL', 'B', 'BR', 'TR'],
             (640, 608): ['BL', 'L', 'R', 'TR'],
             (640, 640): ['BL', 'TL', 'T', 'BR', 'R', 'TR'],
             (640, 704): ['BL', 'B', 'BR'],
             (672, 192): ['T'],
             (672, 320): ['BL', 'B', 'BR'],
             (672, 384): ['TL', 'T', 'TR'],
             (672, 448): ['BL', 'TL', 'B', 'T', 'BR'],
             (672, 576): ['BL', 'B', 'T', 'TR'],
             (672, 704): ['BL', 'B'],
             (704, 192): ['TL'],
             (704, 224): ['L', 'TL'],
             (704, 256): ['BL', 'L', 'TL', 'T', 'TR'],
             (704, 320): ['BL', 'B', 'BR', 'TR'],
             (704, 352): ['R', 'TR'],
             (704, 384): ['TL', 'T', 'BR', 'R', 'TR'],
             (704, 448): ['BL', 'TL', 'B', 'BR', 'R', 'TR'],
             (704, 480): ['L', 'TL', 'BR', 'R', 'TR'],
             (704, 512): ['BL', 'L', 'TL', 'BR', 'R', 'TR'],
             (704, 544): ['BL', 'L', 'BR', 'R'],
             (704, 576): ['BL', 'TL', 'T', 'BR', 'TR'],
             (704, 640): ['BL', 'L', 'TL', 'B', 'BR'],
             (704, 672): ['BL', 'L'],
             (704, 704): ['BL'],
             (736, 256): ['TL', 'T', 'TR'],
             (736, 320): ['BL', 'B', 'T', 'BR'],
             (736, 576): ['TL', 'B', 'T', 'BR', 'TR'],
             (736, 640): ['BL', 'B', 'BR'],
             (768, 128): ['BL', 'TR'],
             (768, 160): ['R', 'TR'],
             (768, 192): ['BR', 'R', 'TR'],
             (768, 224): ['BR', 'R', 'TR'],
             (768, 256): ['TL', 'T', 'BR', 'R', 'TR'],
             (768, 320): ['BL', 'TL', 'B', 'BR'],
             (768, 352): ['L', 'TL'],
             (768, 384): ['BL', 'L', 'TL', 'T', 'TR'],
             (768, 448): ['BL', 'L', 'TL', 'B', 'BR'],
             (768, 480): ['BL', 'L', 'TL'],
             (768, 512): ['BL', 'L', 'TL', 'T', 'TR'],
             (768, 576): ['BL', 'TL', 'B', 'T', 'BR', 'R', 'TR'],
             (768, 640): ['BL', 'B', 'BR'],
             (800, 128): ['T'],
             (800, 320): ['BL', 'B'],
             (800, 384): ['TL', 'T', 'TR'],
             (800, 448): ['BL', 'B', 'BR'],
             (800, 512): ['TL', 'T'],
             (800, 640): ['BL', 'B', 'BR'],
             (832, 128): ['TL', 'TR'],
             (832, 160): ['L', 'TL', 'R', 'TR'],
             (832, 192): ['BL', 'L', 'TL', 'T', 'BR', 'R', 'TR'],
             (832, 256): ['BL', 'L', 'TL', 'B', 'BR'],
             (832, 288): ['BL', 'L'],
             (832, 320): ['BL', 'TR'],
             (832, 352): ['R', 'TR'],
             (832, 384): ['TL', 'T', 'BR', 'R', 'TR'],
             (832, 448): ['BL', 'B', 'BR', 'R', 'TR'],
             (832, 480): ['BR', 'R'],
             (832, 512): ['TL', 'BR'],
             (832, 544): ['L', 'TL'],
             (832, 576): ['BL', 'L', 'TL', 'T', 'TR'],
             (832, 640): ['BL', 'B', 'BR', 'R', 'TR'],
             (832, 672): ['BR', 'R'],
             (832, 704): ['BR'],
             (864, 128): ['T', 'TR'],
             (864, 256): ['BL', 'B'],
             (864, 320): ['T'],
             (864, 512): ['B'],
             (864, 576): ['TL', 'T'],
             (864, 704): ['B', 'BR'],
             (896, 128): ['TL', 'T', 'TR'],
             (896, 192): ['BL', 'L', 'TL', 'B', 'BR', 'R', 'TR'],
             (896, 224): ['BL', 'L', 'BR', 'R', 'TR'],
             (896, 256): ['BL', 'BR', 'R', 'TR'],
             (896, 288): ['BR', 'R'],
             (896, 320): ['TL', 'BR'],
             (896, 352): ['L', 'TL'],
             (896, 384): ['BL', 'L', 'TL'],
             (896, 416): ['BL', 'L', 'TL'],
             (896, 448): ['BL', 'L', 'TL', 'TR'],
             (896, 480): ['BL', 'L', 'R', 'TR'],
             (896, 512): ['BL', 'BR', 'R', 'TR'],
             (896, 544): ['BR', 'R'],
             (896, 576): ['TL', 'BR'],
             (896, 608): ['L', 'TL'],
             (896, 640): ['BL', 'L', 'TL', 'T', 'TR'],
             (896, 704): ['BL', 'B', 'BR'],
             (928, 128): ['TL', 'T', 'TR'],
             (928, 320): ['B', 'BR'],
             (928, 448): ['T', 'TR'],
             (928, 576): ['B'],
             (928, 640): ['TL', 'T', 'TR'],
             (928, 704): ['BL', 'B', 'BR'],
             (960, 128): ['TL', 'T', 'TR'],
             (960, 192): ['BL', 'L', 'TL', 'B', 'BR'],
             (960, 224): ['BL', 'L', 'TL'],
             (960, 256): ['BL', 'L', 'TL', 'T', 'TR'],
             (960, 320): ['BL', 'B', 'BR', 'R', 'TR'],
             (960, 352): ['BR', 'R'],
             (960, 384): ['BR'],
             (960, 448): ['TL', 'T', 'TR'],
             (960, 512): ['BL', 'L', 'TL', 'B', 'BR'],
             (960, 544): ['BL', 'L'],
             (960, 576): ['BL'],
             (960, 640): ['TL', 'T', 'TR'],
             (960, 704): ['BL', 'B', 'BR'],
             (992, 128): ['TL', 'T', 'TR'],
             (992, 192): ['BL', 'B', 'BR'],
             (992, 256): ['TL', 'T'],
             (992, 384): ['B', 'BR'],
             (992, 448): ['TL', 'T', 'TR'],
             (992, 512): ['BL', 'B', 'BR'],
             (992, 640): ['TL', 'T', 'TR'],
             (992, 704): ['BL', 'B', 'BR'],
             (1024, 128): ['TL', 'T', 'TR'],
             (1024, 192): ['BL', 'B', 'BR', 'R', 'TR'],
             (1024, 224): ['BR', 'R'],
             (1024, 256): ['TL', 'BR'],
             (1024, 288): ['L', 'TL'],
             (1024, 320): ['BL', 'L', 'TL', 'T', 'TR'],
             (1024, 384): ['BL', 'B', 'BR', 'R', 'TR'],
             (1024, 416): ['BR', 'R', 'TR'],
             (1024, 448): ['TL', 'T', 'BR', 'R', 'TR'],
             (1024, 512): ['BL', 'B', 'BR', 'TR'],
             (1024, 544): ['R', 'TR'],
             (1024, 576): ['BR', 'R', 'TR'],
             (1024, 608): ['BR', 'R', 'TR'],
             (1024, 640): ['TL', 'T', 'BR', 'R', 'TR'],
             (1024, 704): ['BL', 'B', 'BR'],
             (1056, 128): ['TL', 'T', 'TR'],
             (1056, 256): ['B'],
             (1056, 320): ['TL', 'T', 'TR'],
             (1056, 512): ['BL', 'B', 'T', 'TR'],
             (1056, 704): ['BL', 'B'],
             (1088, 128): ['TL', 'T', 'TR'],
             (1088, 192): ['BL', 'L', 'TL', 'B', 'BR'],
             (1088, 224): ['BL', 'L'],
             (1088, 256): ['BL'],
             (1088, 320): ['TL', 'T', 'TR'],
             (1088, 384): ['BL', 'L', 'TL', 'B', 'BR', 'R', 'TR'],
             (1088, 416): ['BL', 'L', 'TL', 'BR', 'R'],
             (1088, 448): ['BL', 'L', 'TL', 'BR'],
             (1088, 480): ['BL', 'L'],
             (1088, 512): ['BL', 'TL', 'T', 'TR'],
             (1088, 576): ['BL', 'L', 'TL', 'B', 'BR', 'R', 'TR'],
             (1088, 608): ['BL', 'L', 'TL', 'BR', 'R'],
             (1088, 640): ['BL', 'L', 'TL', 'BR'],
             (1088, 672): ['BL', 'L'],
             (1088, 704): ['BL'],
             (1120, 128): ['TL', 'T'],
             (1120, 192): ['BL', 'B'],
             (1120, 320): ['TL', 'T'],
             (1120, 448): ['B'],
             (1120, 512): ['TL', 'T', 'TR'],
             (1120, 640): ['B'],
             (1152, 128): ['TL'],
             (1152, 160): ['L'],
             (1152, 192): ['BL'],
             (1152, 320): ['TL'],
             (1152, 352): ['L', 'TL'],
             (1152, 384): ['BL', 'L', 'TL'],
             (1152, 416): ['BL', 'L'],
             (1152, 448): ['BL'],
             (1152, 512): ['TL', 'T'],
             (1152, 576): ['BL', 'L', 'TL', 'B'],
             (1152, 608): ['BL', 'L'],
             (1152, 640): ['BL'],
             (1184, 512): ['TL'],
             (1184, 544): ['L'],
             (1184, 576): ['BL']}


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


# def return_imageText(image, text):
#     imageDraw = ImageDraw.Draw(image)
#     font = ImageFont.truetype('arial', 20)
#     imageDraw.text((5, 5), text, font=font, fill=(128, 128, 128))
#     return image

# main


def return_lighting_tile(TOP_image, TOPR_image, neighbour):
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


def set_images():
    image_types = ["T", "R", "B", "L", "TR", "BR", "BL", "TL"]
    for i in image_types:
        imagesADI[i + "_image"] = return_lighting_tile(T_image, TR_image, i)


def return_blended(neighbours01, neighbours02):
    forgound_image = neighbours01
    background_image = neighbours02
    forground_array = return_array(forgound_image)
    background_array = return_array(background_image)
    res = return_darken(forground_array, background_array)
    return res

def set_route_light_positions_tiles(dict):
    route_light_positions_tiles = dict
    # print("len(dict)", len(dict))
    for k, v in dict.items():
        # print("v", v)
        if len(v) == 1:
            # print("len(v) == 1")
            res = return_lighting_tile(T_image, TR_image, v[-1])
            route_light_positions_tiles[k] = res
        elif len(v) == 2:
            # print("len(v) == 2")
            res = return_blended(imagesADI[v[0] + "_image"], imagesADI[v[1] + "_image"])
            route_light_positions_tiles[k] = res
        elif len(v) > 2:
            # print("len(v) > 2")
            fore = imagesADI[v.pop() + "_image"]
            while len(v) > 0:
                back = imagesADI[v.pop() + "_image"]
                blend = return_blended(fore, back)
                res = blend
            route_light_positions_tiles[k] = res
    print("set_route_light_positions_tiles - DONE!!!!!!!")

            




set_images()
set_route_light_positions_tiles(ADITESTDICT)



# blended_image = return_blended(imagesADI["T_image"], imagesADI["R_image"])

# blended_image02 = return_blended(blended_image, imagesADI["B_image"])


# blended_image.show()
# blended_image02.show()


# print("ADITESTDICT", type(ADITESTDICT))
# print("ADITESTDICT", type(ADITESTDICT))