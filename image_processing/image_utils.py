import numpy as np
import base64
from io import BytesIO
from PIL import Image, ImageDraw,ImageFont
import cv2
import sympy

def decode_image(img_str):
    """Decodes an image from a b64 image string.
    Args:
        img_str (str): An image represented as a b64 string.
    Returns:
        ndarray: An image represented as a ndarray (PIL Image format).
    """
    decoded = base64.b64decode(img_str.split("base64,")[-1])
    image = Image.open(BytesIO(decoded))
    #image = np.asarray(image)
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def encode_image(image):
    """Encodes an image to b64 string format.
    Args:
        image (ndarray): An image in array format (can be read by opencv library).
    Returns:
        str: Data representing an image in a b64 string format.
    """
    # convert opencv image to PIL
    # img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # im_pil = Image.fromarray(img)

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    b64_string = base64.b64encode(buffered.getvalue())
    b64_string = "data:image/jpeg;base64," + b64_string.decode()
    return b64_string

def draw_equations(image, equations_list):
    img = image.copy()
    drw = ImageDraw.Draw(img)

    for equation in equations_list:
        print(equation)
        print("result is:", equation.result[0], equation.result[1])
        drw.rectangle([(equation.eq_coord[1], equation.eq_coord[2]), (equation.eq_coord[3], equation.eq_coord[4])], outline="red")
        X_result=equation.eq_coord[3] +20
        Y_result=abs((equation.eq_coord[2] - equation.eq_coord[4])/2)
        Y_result=max(equation.eq_coord[2], equation.eq_coord[4])-Y_result

        font = ImageFont.truetype("arial.ttf", 26)
        drw.text((X_result, Y_result), str(equation.result[1]), font=font, fill ="black", align ="left")

        for entry in equation():
            drw.rectangle([(entry[1], entry[2]), (entry[3], entry[4])], outline="blue")
    return img