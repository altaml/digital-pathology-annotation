import logging
from openslide import OpenSlide
import numpy as np
import cv2
from PIL import Image


def read_svs(fpath, show_info=False, thumbnail_only=True):
    '''
    Read the slide image from .svs file. Returns thumbnail and optionally high resolution images of tissues
    :param {Path} fpath: Path to the location of the svs file to be read.
    :param {bool} show_info: If set prints metadata about svs.
    :param {bool} thumbail_only: If set returns only thumbail of svs.
    '''
    try:
        logging.info('Thumbnail image being read')
        slide_image = OpenSlide(str(fpath))
        if show_info:
            print('Level Count', slide_image.level_count)
            print('Resolutions', slide_image.level_dimensions)
            print('Scale', slide_image.level_downsamples)
        level = slide_image.level_count - 1
        scale_factor = int(slide_image.level_downsamples[-1])
        img_size = slide_image.level_dimensions[-1]
        thumbnail = np.uint8(
            np.array(
                slide_image.read_region(
                    (0, 0),
                    level,
                    img_size,
                )
            )[:, :, :3]
        )
        if thumbnail_only:
            logging.warn(
                'svs reader is only generating thumbails. Tissues not generated.'
            )
            return [], thumbnail
        logging.info('High magnification processing. Tissue extraction')
        cropped_cells, bbox = _isolate_cells_tissues_from_svs(
            image=thumbnail,
            return_coords=True,
            show_thresholded=False,
        )
        high_rez_cropped_cells = []
        for boundRect in bbox:
            # Check for minimum size
            x, y, width, height = boundRect
            logging.info(
                f'High rez dimensions: {scale_factor*(width)}, {scale_factor*(height)}'
            )
            logging.info(
                f'Size conversion: {[x,y,x+width,y+width]}:{[scale_factor*x, scale_factor*y,scale_factor*(x+width), scale_factor*(y+height)]} '
            )

            img = np.uint8(
                np.array(
                    slide_image.read_region(
                        (scale_factor * x, scale_factor * y),
                        0,
                        (scale_factor * (width), scale_factor * (height)),
                    )
                )[:, :, :3]
            )
            logging.info(f'Image extracted {img.shape}')
            high_rez_cropped_cells.append(img)
        logging.info(f'Generated {len(high_rez_cropped_cells)} tissues')
        return high_rez_cropped_cells, thumbnail

    except IOError as e:
        logging.error(f'Cant read {fpath}. {e}')
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
