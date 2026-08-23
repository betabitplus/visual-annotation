"""Customize point annotations
===========================

Apply a one-off appearance configuration while marking normalized points on an
image. Passing ``config=`` changes only this annotation call.
"""
# sphinx_gallery_tags = ["points", "config", "images", "annotation"]

from __future__ import annotations

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

from visual_annotation import VisualAnnotationConfig, VisualPoint, annotate

POINTS = [
    VisualPoint(label="car", coord=[0.26, 0.74]),
    VisualPoint(label="truck", coord=[0.75, 0.56]),
]
CONFIG = VisualAnnotationConfig(
    annotation_color="BLUE",
    label_color="WHITE",
    point_radius=8,
)


# %%
# Build the input image
# ---------------------
def build_scene() -> Image.Image:
    """Return a small road scene as a plain RGB image."""
    image = Image.new("RGB", (640, 360), "#dbeafe")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 220, 640, 360), fill="#52525b")
    draw.rounded_rectangle((122, 234, 218, 299), radius=8, fill="#d4d4d8")
    draw.rounded_rectangle((435, 155, 525, 248), radius=8, fill="#a1a1aa")
    return image


# %%
# Pass appearance for this call
# -----------------------------
# The core behavior is still ``annotate()``. Supplying ``config`` changes the
# point color and radius without changing the process-wide defaults.
if __name__ == "__main__":
    image = build_scene()
    response = annotate(image, POINTS, config=CONFIG)

    print(f"elements: {response.element_count}")
    print(f"point radius: {CONFIG.point_radius}")

    figure, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].imshow(image)
    axes[0].set_title("Input")
    axes[1].imshow(response.response_data)
    axes[1].set_title("Custom point style")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()

# %%
# The output makes the call-local appearance visible while leaving the library's
# installed defaults untouched for later annotation calls.
