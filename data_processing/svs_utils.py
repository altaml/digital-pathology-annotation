import logging
from openslide import OpenSlide
import numpy as np
import cv2


def read_svs(fpath, show_info=False):
    """
    Read the slide image from .svs file
    :param {Path} fpath: Path to the location of the svs file to be read.
    :param {bool} show_info: If set prints metadata about svs.
    """
    try:
        slide_image = OpenSlide(str(fpath))
        if show_info:
            print(slide_image.level_count)
            print(slide_image.level_dimensions)
            print(slide_image.level_downsamples)

        image = np.uint8(
            np.array(
                slide_image.read_region(
                    (0, 0),
                    slide_image.level_count - 1,
                    slide_image.level_dimensions[-1],
                )
            )[:, :, :3]
        )
        logging.info("Image read successfully")
        return image

    except IOError as e:
        logging.error(f"Cant read {fpath}. {e}")
        raise IOError(e)
