import yaml


def load_video_config():
    with open(
        "config/video.yaml",
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)
