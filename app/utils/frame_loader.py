import os
import re
from typing import Tuple
from rich_pixels import FullcellRenderer, Pixels
from PIL import Image


def load_avatar(character_name: str, resize: Tuple[int, int]):
    """
    Recursively check images/ folder for:
    <character_name>/ -- parent folder with avatar name
    |   <animation_name>/ -- subfolder with the name of the animations
    |   |   <direction>/ -- direciton of avatar: up, down, side(facing-right)
    Will load all frames within this directory.
    """
    file_path = f"images/{character_name}"
    memo = {}

    # ['idle', 'walk']
    animation_names = os.listdir(file_path)

    for animation_name in animation_names:
        if animation_name not in memo:
            memo[animation_name] = {}
        animation_path = f"{file_path}/{animation_name}"

        # ['up', 'down', 'side']
        directions = os.listdir(animation_path)

        for direction in directions:
            if direction not in memo[animation_name]:
                memo[animation_name][direction] = []

            direction_path = f"{animation_path}/{direction}"
            frames = os.listdir(direction_path)

            for frame in frames:
                frame_path = f"{direction_path}/{frame}"
                memo[animation_name][direction].append(
                    load_frame(frame_path, resize=resize)
                )

    return memo


def resize_image_pil(file_path: str, resize: Tuple[int, int]) -> Image.Image:
    """Resize the image using PIL while maintaining aspect ratio"""
    image = Image.open(file_path)
    width, height = image.size
    aspect_ratio = width / height
    target_width, target_height = resize

    if target_width / target_height > aspect_ratio:
        target_width = int(target_height * aspect_ratio)
    else:
        target_height = int(target_width / aspect_ratio)

    return image.resize((target_width, target_height), Image.Resampling.NEAREST)


def load_frame(file_path: str, resize: Tuple[int, int]) -> Pixels:
    """
    Render frames uses Rich Pixels to load frams from file path
    Directory must have frames names robo-1.png to robo-12.png
    Returns a list of Rich Pixels
    """
    image = resize_image_pil(file_path, resize)
    return Pixels.from_image(image, renderer=FullcellRenderer())
