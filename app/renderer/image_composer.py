import json
import subprocess
from pathlib import Path

from app.ffmpeg import FFMPEG
from app.motion import MotionEngine


WIDTH = 1080
HEIGHT = 1920

FPS = 30

CRF = 20
PRESET = "medium"

VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"


class ImageComposer:

    def __init__(self):

        self.motion = MotionEngine()

    def load_metadata(
        self,
        image_folder: str,
    ):

        metadata_file = (
            Path(image_folder)
            / "metadata.json"
        )

        if not metadata_file.exists():

            raise FileNotFoundError(
                metadata_file
            )

        with open(
            metadata_file,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def build_inputs(
        self,
        metadata,
        image_folder,
        audio_path,
    ):

        command = []

        for item in metadata:

            duration = float(
                item["duration"]
            )

            image = (
                Path(image_folder)
                / item["file"]
            )

            command.extend(

                [

                    "-loop",
                    "1",

                    "-t",
                    str(duration),

                    "-i",
                    str(image),

                ]

            )

        command.extend(

            [

                "-i",

                audio_path,

            ]

        )

        return command

    def build_filters(
        self,
        metadata,
    ):

        self.motion.reset()

        filters = []

        outputs = []

        for index, item in enumerate(metadata):

            duration = float(
                item["duration"]
            )

            motion = self.motion.build_filter(

                duration=duration,

                fps=FPS,

            )

            print(
                f"Motion : {motion}"
            )

            filters.append(

                (
                    f"[{index}:v]"

                    "scale=1080:1920:"
                    "force_original_aspect_ratio=increase,"

                    "crop=1080:1920,"

                    f"{motion},"

                    f"trim=duration={duration},"

                    "setpts=PTS-STARTPTS"

                    f"[v{index}]"
                )

            )

            outputs.append(
                f"[v{index}]"
            )

        return filters, outputs
import json
import subprocess
from pathlib import Path

from app.ffmpeg import FFMPEG
from app.motion import MotionEngine


WIDTH = 1080
HEIGHT = 1920

FPS = 30

CRF = 20
PRESET = "medium"

VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"


class ImageComposer:

    def __init__(self):

        self.motion = MotionEngine()

    def load_metadata(
        self,
        image_folder: str,
    ):

        metadata_file = (
            Path(image_folder)
            / "metadata.json"
        )

        if not metadata_file.exists():

            raise FileNotFoundError(
                metadata_file
            )

        with open(
            metadata_file,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def build_inputs(
        self,
        metadata,
        image_folder,
        audio_path,
    ):

        command = []

        for item in metadata:

            duration = float(
                item["duration"]
            )

            image = (
                Path(image_folder)
                / item["file"]
            )

            command.extend(

                [

                    "-loop",
                    "1",

                    "-t",
                    str(duration),

                    "-i",
                    str(image),

                ]

            )

        command.extend(

            [

                "-i",

                audio_path,

            ]

        )

        return command

    def build_filters(
        self,
        metadata,
    ):

        self.motion.reset()

        filters = []

        outputs = []

        for index, item in enumerate(metadata):

            duration = float(
                item["duration"]
            )

            motion = self.motion.build_filter(

                duration=duration,

                fps=FPS,

            )

            print(
                f"Motion : {motion}"
            )

            filters.append(

                (
                    f"[{index}:v]"

                    "scale=1080:1920:"
                    "force_original_aspect_ratio=increase,"

                    "crop=1080:1920,"

                    f"{motion},"

                    f"trim=duration={duration},"

                    "setpts=PTS-STARTPTS"

                    f"[v{index}]"
                )

            )

            outputs.append(
                f"[v{index}]"
            )

        return filters, outputs