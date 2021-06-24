from pathlib import Path
from typing import Iterator, List, Tuple

import cv2
import numpy as np
from joblib import Parallel, delayed
from skimage.metrics import structural_similarity

from reverse_image_search import config


def load_image(path: Path, grayscale=True) -> np.ndarray:
    if grayscale:
        img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(str(Path))
    return img


def resize_image(
    img: np.ndarray, dim: Tuple = (config.RESIZE_HEIGHT, config.RESIZE_WIDTH)
) -> np.ndarray:
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def walk(path: Path) -> Iterator[Path]:
    if path.is_file():
        return path

    for p in path.iterdir():
        if p.is_symlink():
            # Do not follow symlinks, or you might end up recursing indefinitely
            continue
        try:
            is_dir = p.is_dir()
        except OSError:  # Occurs when you can't "stat" a file
            continue
        if is_dir:
            try:
                yield from walk(p)
            except PermissionError:
                # Ignore files we can't access
                pass
            continue
        yield p


def get_similarity(src: np.ndarray, filepath: Path) -> Tuple[Path, float]:
    target = load_image(filepath)
    if target is None:  # unable to load image
        return filepath, 0
    target = resize_image(target)
    similarity = structural_similarity(src, target)
    return filepath, similarity


def search_similar_images(
    src_path: Path,
    search_path: Path,
    threshold: float,
    allowed_filetypes=List[str],
) -> List[Tuple[Path, float]]:
    # load first image only once
    src = load_image(src_path)
    src = resize_image(src)

    # Get results using multiprocessing
    results = Parallel(n_jobs=-1)(
        delayed(get_similarity)(src, filepath)
        for filepath in walk(search_path)
        if filepath.suffix.lower() in allowed_filetypes
    )

    results = [
        (filepath, similarity)
        for filepath, similarity in results
        if similarity >= threshold
    ]

    return results
