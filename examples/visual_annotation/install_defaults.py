"""Install shared annotation defaults
==================================

Install one immutable appearance snapshot for repeated calls, then use the normal
``annotate()`` entrypoint without passing ``config=`` each time.
"""
# sphinx_gallery_tags = ["config", "defaults", "boxes", "annotation"]

from __future__ import annotations

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

from visual_annotation import (
    AnnotationResponse,
    VisualAnnotationConfig,
    VisualBox,
    annotate,
    get_config,
    install_config,
)

BOX = VisualBox(label="car", coord=[0.19, 0.65, 0.34, 0.83])
SHARED_CONFIG = VisualAnnotationConfig(annotation_color="GREEN", box_thickness=5)


def build_scene() -> Image.Image:
    """Return a small road scene as a plain RGB image."""
    image = Image.new("RGB", (640, 360), "#dbeafe")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 220, 640, 360), fill="#52525b")
    draw.rounded_rectangle((122, 234, 218, 299), radius=8, fill="#d4d4d8")
    draw.rounded_rectangle((435, 155, 525, 248), radius=8, fill="#a1a1aa")
    return image


# %%
# Install a process-wide snapshot safely
# --------------------------------------
# ``install_config()`` is useful when many calls should share the same appearance.
# This runnable example restores the previous snapshot afterwards so importing or
# executing it never leaves process-global state behind.
def annotate_with_shared_defaults(image: Image.Image) -> AnnotationResponse:
    """Annotate once through a temporarily installed shared config."""
    previous = get_config()
    try:
        install_config(SHARED_CONFIG)
        return annotate(image, [BOX])
    finally:
        install_config(previous)


# %%
# Use the ordinary annotation call path
# -------------------------------------
# The helper above installs the shared config before ``annotate()``; callers that
# own the whole process can install it once during application startup instead.
if __name__ == "__main__":
    image = build_scene()
    response = annotate_with_shared_defaults(image)

    print(f"elements: {response.element_count}")
    print(f"shared box thickness: {SHARED_CONFIG.box_thickness}")

    figure, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].imshow(image)
    axes[0].set_title("Input")
    axes[1].imshow(response.response_data)
    axes[1].set_title("Installed defaults")
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()

# %%
# The green, thicker box is proof that the installed snapshot was used even though
# the annotation call itself did not receive a ``config`` argument.
