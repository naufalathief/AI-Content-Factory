from app.schemas import Script


def calculate_scene_duration(
    script: Script,
    total_duration: float,
):
    total_chars = sum(
        len(scene.text)
        for scene in script.scenes
    )

    for scene in script.scenes:

        ratio = len(scene.text) / total_chars

        scene.duration = round(
            ratio * total_duration,
            2,
        )

    return script
