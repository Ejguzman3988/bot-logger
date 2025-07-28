from typing import List, Tuple
from rich_pixels import FullcellRenderer, Pixels


def load_frames(
    folder_path: str, resize: Tuple[int, int] | None = None
) -> List[Pixels]:
    """
    Render frames uses Rich Pixels to load frams from file path
    Directory must have frames names robo-1.png to robo-12.png
    Returns a list of Rich Pixels
    """

    frames = []
    for i in range(1, 13):
        frame_path = f"{folder_path}/robo-{i}.png"
        frame = Pixels.from_image_path(
            frame_path, resize=resize, renderer=FullcellRenderer()
        )
        frames.append(frame)

    return frames
