from pathlib import Path

from app.motion.ffmpeg_builder import (
    FFmpegBuilder,
)
from app.motion.models import (
    MotionClip,
    MotionFilter,
)
from app.motion.selector import (
    MotionSelector,
)


FPS = 30


class MotionEngine:

    def __init__(self):

        self.selector = MotionSelector()

    def build_clip(

        self,

        index: int,

        image: Path,

        duration: float,

    ) -> MotionClip:

        preset = self.selector.select()

        frames = max(
            int(duration * FPS),
            1,
        )

        expression = (
            preset.expression
            .replace(
                "{frames}",
                str(frames),
            )
        )

        clip = MotionClip(

            input_index=index,

            image_path=str(image),

            duration=duration,

            output_label=f"v{index}",

        )

        clip.filters.append(

            MotionFilter(

                name=preset.name,

                expression=expression,

            )

        )

        return clip

    def build_graph(

        self,

        metadata,

        image_folder,

    ):

        self.selector.reset()

        clips = []

        for index, item in enumerate(metadata):

            clips.append(

                self.build_clip(

                    index=index,

                    image=Path(image_folder)
                    / item["file"],

                    duration=item["duration"],

                )

            )

        return clips

    def build_filter_complex(
        self,
        clips,
    ):

        filters = [

            FFmpegBuilder.build_filter(
                clip
            )

            for clip in clips

        ]

        outputs = "".join(

            f"[{c.output_label}]"

            for c in clips

        )

        filters.append(

            f"{outputs}"
            f"concat=n={len(clips)}:"
            "v=1:a=0,format=yuv420p[v]"

        )

        return ";".join(filters)