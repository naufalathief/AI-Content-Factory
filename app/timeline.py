import json


def build_timeline(script, audio_duration):
    scenes = script.scenes

    total_words = sum(
        len(scene.text.split())
        for scene in scenes
    )

    current = 0.0

    timeline = []

    for index, scene in enumerate(scenes):

        words = len(scene.text.split())

        duration = (
            words / total_words
        ) * audio_duration

        timeline.append(
            {
                "scene": index + 1,
                "keyword": scene.keyword,
                "text": scene.text,
                "start": round(current, 2),
                "end": round(current + duration, 2),
            }
        )

        current += duration

    return timeline


def save_timeline(path, timeline):
    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            timeline,
            file,
            indent=4,
            ensure_ascii=False,
        )
