from app.timeline.timeline_builder import TimelineBuilder


def run(
    video_id: int,
):

    builder = TimelineBuilder()

    return builder.build(
        video_id
    )