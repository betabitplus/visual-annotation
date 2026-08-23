"""Overlay a segmentation mask
============================

Turn a boolean image-sized mask into a labeled visual overlay. The mask stays a
plain nested boolean structure at the public API boundary.
"""
# sphinx_gallery_tags = ["masks", "segmentation", "images", "annotation"]

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from visual_annotation import VisualMask, annotate


# %%
# Build an image-sized boolean mask
# ---------------------------------
# Here the rectangle covers the car in the example image. Real callers can pass
# the same nested boolean shape from any segmentation model or image pipeline.
def build_car_mask(image: Image.Image) -> list[list[bool]]:
    """Return a boolean mask covering the car region."""
    mask = np.zeros((image.height, image.width), dtype=bool)
    x1, y1, x2, y2 = (
        round(0.19 * image.width),
        round(0.65 * image.height),
        round(0.34 * image.width),
        round(0.83 * image.height),
    )
    mask[y1:y2, x1:x2] = True
    return mask.tolist()


def build_scene() -> Image.Image:
    """Return a small road scene as a plain RGB image."""
    image = Image.new("RGB", (640, 360), "#dbeafe")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 220, 640, 360), fill="#52525b")
    draw.rounded_rectangle((122, 234, 218, 299), radius=8, fill="#d4d4d8")
    draw.rounded_rectangle((435, 155, 525, 248), radius=8, fill="#a1a1aa")
    return image


# %%
# Annotate the mask and inspect the result
# ----------------------------------------
# ``VisualMask`` carries the segmentation payload; ``annotate()`` handles the
# rendering and returns the same response shape used by boxes and points.
if __name__ == "__main__":
    image = build_scene()
    elements = [VisualMask(label="car", coord=build_car_mask(image))]
    response = annotate(image, elements)

    print(f"elements: {response.element_count}")
    print(f"output size: {response.response_data.size}")

    figure, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].imshow(image)
    axes[0].set_title("Input")
    axes[1].imshow(response.response_data)
    axes[1].set_title("Annotated mask")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()

# %%
# The visible overlay comes from the same boolean mask supplied to ``VisualMask``;
# no private supervision/OpenCV objects leak into caller code.
