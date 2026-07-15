import json
from pathlib import Path


class TimelineBuilder:

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    def build(
        self,
        video_id: int,
    ) -> Path:

        image_dir = (
            Path("storage")
            / "images"
            / str(video_id)
        )

        metadata_file = (
            image_dir
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

            metadata = json.load(file)

        clips = []

        current_time = 0.0
        current_frame = 0

        for index, item in enumerate(metadata):

            duration = float(
                item["duration"]
            )

            frames = round(
                duration * self.FPS
            )

            clips.append(

                {

                    "index": index,

                    # Docker path
                    "image": f"/storage/images/{video_id}/{item['file']}",

                    "startTime": current_time,

                    "startFrame": current_frame,

                    "duration": duration,

                    "durationFrames": frames,

                }

            )

            current_time += duration
            current_frame += frames

        timeline = {

            "videoId": video_id,

            "width": self.WIDTH,

            "height": self.HEIGHT,

            "fps": self.FPS,

            "totalDuration": current_time,

            "totalFrames": current_frame,

            # Docker path
            "audio": f"/storage/voices/{video_id}.mp3",

            "subtitle": f"/storage/subtitles/{video_id}.srt",

            "clips": clips,

        }

        output_dir = (
            Path("storage")
            / "timeline"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = (
            output_dir
            / f"{video_id}.json"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                timeline,
                file,
                indent=4,
                ensure_ascii=False,
            )

        print("=" * 60)
        print("TIMELINE GENERATED")
        print("=" * 60)
        print(output)

        return output