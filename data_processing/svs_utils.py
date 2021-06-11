import logging
from openslide import OpenSlide
import numpy as np
import cv2
from PIL import Image


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

# Helper functions
def _isolate_cells_tissues_from_svs(
    image,
    show_thresholded=False,
    fn=0,
    return_coords=False,
):
    '''
    Crop tissue from an image. Return tissue only if size criteria is met.
    Uses threshold to get the tissue outline from the slide background.
    Connected component analysis is used on the thresholded image to isolate
    individual tissues.
    '''
    MIN_TISSUE_SIZE_LOW_REZ_DYNALIFE = 100
    MAX_TISSUE_SIZE_LOW_REZ_DYNALIFE = 300
    bb = getmarkerboundingrect(image, show_thresholded, fn)
    cropped_cells = []
    bb_final = []
    for boundRect in bb:
        # Check for minimum size
        if (
            (boundRect[3] > MIN_TISSUE_SIZE_LOW_REZ_DYNALIFE)
            and (boundRect[2] > MIN_TISSUE_SIZE_LOW_REZ_DYNALIFE)
            and (boundRect[3] < int(image.shape[0] * 0.9))
            and (boundRect[2] < int(image.shape[1] * 0.5))
        ):
            bb_final.append(boundRect)
            x, y, width, height = boundRect
            # Remove too large tissues
            if (
                np.min(image[y : y + height, x : x + width])
                < MAX_TISSUE_SIZE_LOW_REZ_DYNALIFE
            ):
                cropped_image = Image.fromarray(image[y : y + height, x : x + width])
                cropped_cells.append(cropped_image)
    logging.info(f'Found {len(cropped_cells)} tissues.')

    if return_coords:
        return cropped_cells, bb_final
    else:
        return cropped_cells, None


def thresold(img, gaussian_window=3, C=3, morphological_window=3):
    '''Performs an adaptive thresholding to isolate tissue regions from the slide.'''
    th = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        gaussian_window,
        C,
    )
    kernel = np.ones((morphological_window, morphological_window), np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    opening = cv2.medianBlur(opening, 15)
    return 255 - opening


def getmarkerboundingrect(image, show, fn):
    '''
    Get boundaries of thresholded tissues
    '''
    gray = np.uint8(np.mean(np.float32(image), axis=2))
    binimage = thresold(gray)
    if show:
        cv2.imwrite('thres.jpg', binimage)
    nlabels, _, stats, _ = cv2.connectedComponentsWithStats(binimage)
    bbs = []
    for label in range(nlabels):
        # retrieving the width of the bounding box of the component
        width = stats[label, cv2.CC_STAT_WIDTH]
        # retrieving the height of the bounding box of the component
        height = stats[label, cv2.CC_STAT_HEIGHT]
        # retrieving the leftmost coordinate of the bounding box of the component
        x = stats[label, cv2.CC_STAT_LEFT]
        # retrieving the topmost coordinate of the bounding box of the component
        y = stats[label, cv2.CC_STAT_TOP]
        bbs.append((x, y, width, height))
    return bbs
