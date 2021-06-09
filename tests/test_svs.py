from data_processing.svs_utils import read_svs
from pathlib import Path
import os
import cv2
import numpy as np


def test_svs_reader_reads():
    file_path = Path("tests") / "sample_data" / "small.svs"
    img = read_svs(file_path)
    assert len(img.shape) == 3
    assert img.shape == (16, 16, 3)


def test_conversion_script_jpg():
    os.system(
        "python data_processing/convert.py --path tests/sample_data --format .jpg --output_dir converted"
    )
    image_file = Path("converted") / "small.jpg"
    assert image_file.is_file()
    read_back = cv2.imread(str(image_file))
    assert read_back.shape == (16, 16, 3)
    h, w, c = read_back.shape
    black_pixel_percent = np.sum(np.int32(read_back == 0)) / (h * w * c)
    assert black_pixel_percent < 0.1
    image_file.unlink()
    Path("converted").rmdir()


def test_conversion_script_png():
    os.system(
        "python data_processing/convert.py --path tests/sample_data --format .png --output_dir converted"
    )
    image_file = Path("converted") / "small.png"
    assert image_file.is_file()
    read_back = cv2.imread(str(image_file))
    assert read_back.shape == (16, 16, 3)
    h, w, c = read_back.shape
    black_pixel_percent = np.sum(np.int32(read_back == 0)) / (h * w * c)
    assert black_pixel_percent < 0.1
    image_file.unlink()
    Path("converted").rmdir()
