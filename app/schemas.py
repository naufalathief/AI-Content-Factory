from dataclasses import dataclass
from typing import List


@dataclass
class Scene:
    text: str
    keyword: str
    duration: float = 0.0


@dataclass
class Script:
    title: str
    scenes: List[Scene]
    cta: str

    @classmethod
    def from_dict(cls, data: dict):
        scenes = [
            Scene(
                text=item["text"],
                keyword=item["keyword"],
                duration=item.get(
                    "duration",
                    0.0,
                ),
            )
            for item in data["scenes"]
        ]

        return cls(
            title=data["title"],
            scenes=scenes,
            cta=data["cta"],
        )

    def to_dict(self):
        return {
            "title": self.title,
            "scenes": [
                {
                    "text": scene.text,
                    "keyword": scene.keyword,
                    "duration": scene.duration,
                }
                for scene in self.scenes
            ],
            "cta": self.cta,
        }
