# Python imports
from io import BytesIO
from os.path import join

# Django imports
from django.core.files import File
from django.db import models

# external imports
from PIL import Image


def thumbnail_image(image):
    FILE_SIZE = (150, 150)

    file_extension = image.name.split(".")[-1]
    image_name = image.name.split("/")[-1]

    thumbnail_image_name = (
        "".join(image_name.split(".")[::-1][1:][::-1])
        + "_thumb."
        + file_extension
    )
    thumbnail_image_path = join(
        "/".join(image.path.split("/")[::-1][1:][::-1]), thumbnail_image_name
    )

    image = Image.open(image)
    image.thumbnail(FILE_SIZE, Image.ANTIALIAS)
    image.save(thumbnail_image_path)

    return "/".join(thumbnail_image_path.split("/")[::-1][:3][::-1])


# image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.convert("RGB").save(im_io, "JPEG", quality=60)
    new_image = File(im_io, name=image.name.split("/")[-1])
    return new_image
