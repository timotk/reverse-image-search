from pathlib import Path

import numpy as np
import pytest

from reverse_image_search import search


@pytest.fixture
def image_path():
    return Path("images")


def test_load_image(image_path):
    img = search.load_image(image_path / "hills-2836301_1920.jpg")
    assert img.shape == (1200, 1920)


def test_walk(image_path):
    iterator = search.walk(image_path)
    items = sorted(list(iterator))  # order differs per OS
    assert (image_path / "hills-2836301_1920.jpg") in items
    assert (image_path / "hills-2836301_1920_thumbnail.jpg") in items


def test_resize_image():
    img = np.array(
        [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], dtype="uint8"
    )
    expected = np.array(
        [
            [2, 4],
            [2, 4],
        ],
        dtype="uint8",
    )

    dim = (2, 2)
    resized_img = search.resize_image(img, dim=dim)
    assert resized_img.shape == dim
    np.testing.assert_array_equal(resized_img, expected)
