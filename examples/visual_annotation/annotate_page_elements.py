"""Outline document page elements
==============================

Annotate positioned document regions with the same normalized-coordinate API used
for visual detections. ``PageElement`` carries content without requiring labels.
"""
# sphinx_gallery_tags = ["page-elements", "documents", "images", "annotation"]

from __future__ import annotations

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

from visual_annotation import PageElement, annotate

ELEMENTS = [
    PageElement(coord=[0.08, 0.12, 0.92, 0.30], content="Quarterly report"),
    PageElement(coord=[0.08, 0.38, 0.92, 0.82], content="Revenue grew by 18 percent."),
]


# %%
# Build a small document-like image
# ---------------------------------
# The example image is generated locally so the page-element workflow stays fully
# hermetic and can be executed without downloads or fixtures.
def build_document() -> Image.Image:
    """Return a simple document-like RGB image."""
    image = Image.new("RGB", (640, 360), "white")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((45, 35, 595, 325), radius=16, fill="#f4f4f5")
    draw.text((70, 65), "Quarterly report", fill="#18181b")
    draw.text((70, 165), "Revenue grew by 18 percent.", fill="#3f3f46")
    draw.text((70, 205), "Operating margin improved.", fill="#3f3f46")
    return image


# %%
# Annotate positioned regions
# ----------------------------
# The core call is identical to visual boxes. Page elements are rendered as regions
# while their text content remains part of the caller-owned DTO.
if __name__ == "__main__":
    image = build_document()
    response = annotate(image, ELEMENTS)

    print(f"elements: {response.element_count}")
    print(f"first content: {ELEMENTS[0].content}")

    figure, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].imshow(image)
    axes[0].set_title("Document")
    axes[1].imshow(response.response_data)
    axes[1].set_title("Page regions")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()

# %%
# The result makes document geometry visible without forcing page-extraction details
# into the annotation API or inventing visual labels for text regions.
