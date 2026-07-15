from app.motion.models import MotionClip


class FFmpegBuilder:

    @staticmethod
    def build_filter(
        clip: MotionClip,
    ) -> str:

        chain = []

        chain.append(
            "scale=1080:1920:"
            "force_original_aspect_ratio=increase"
        )

        chain.append(
            "crop=1080:1920"
        )

        chain.extend(
            f.expression
            for f in clip.filters
        )

        chain.append(
            "fps=30"
        )

        chain.append(
            f"trim=duration={clip.duration}"
        )

        chain.append(
            "setpts=PTS-STARTPTS"
        )

        return (
            f"[{clip.input_index}:v]"
            + ",".join(chain)
            + f"[{clip.output_label}]"
        )