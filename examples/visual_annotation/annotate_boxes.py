"""Draw labeled bounding boxes
===========================

Add normalized bounding boxes to a PIL image and inspect the annotated result.
The public API keeps coordinates independent of the source image dimensions.
"""
# sphinx_gallery_tags = ["boxes", "images", "annotation"]

from __future__ import annotations

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

from visual_annotation import VisualBox, annotate

BOXES = [
    VisualBox(label="car", coord=[0.19, 0.65, 0.34, 0.83]),
    VisualBox(label="truck", coord=[0.68, 0.43, 0.82, 0.69]),
]


# %%
# Build an ordinary PIL image
# ---------------------------
# The input is deliberately generated with Pillow so the example stays standalone.
# Coordinates stay normalized, so callers never need to convert them to pixels.
def build_scene() -> Image.Image:
    """Return a small road scene as a plain RGB image."""
    image = Image.new("RGB", (640, 360), "#dbeafe")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 220, 640, 360), fill="#52525b")
    draw.rounded_rectangle((122, 234, 218, 299), radius=8, fill="#d4d4d8")
    draw.rounded_rectangle((435, 155, 525, 248), radius=8, fill="#a1a1aa")
    return image


# %%
# Annotate and inspect the result
# -------------------------------
# ``annotate()`` is the core action. It returns a new image plus public metadata;
# the source image remains available for comparison.
if __name__ == "__main__":
    image = build_scene()
    response = annotate(image, BOXES)

    print(f"elements: {response.element_count}")
    print(f"output size: {response.response_data.size}")

    figure, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].imshow(image)
    axes[0].set_title("Input")
    axes[1].imshow(response.response_data)
    axes[1].set_title("Annotated boxes")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()

# %%
# The result keeps the original image size while making both labeled regions
# visible. The same normalized coordinates work for any image with the same scene.
