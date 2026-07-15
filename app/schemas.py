from dataclasses import dataclass


@dataclass
class Visual:

    prompt: str

    duration: float

@dataclass
class Scene:

    text: str

    keyword: str

    visuals: list[Visual]

    duration: float = 0.0


@dataclass
class Script:

    title: str

    scenes: list[Scene]

    cta: str

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        scenes = [

            Scene(

                text=item["text"],

                keyword=item["keyword"],

                visuals=[

                    Visual(

                        prompt=v["prompt"],

                        duration=v["duration"]

                    )

                    for v in item["visuals"]

                ],

                duration=item.get("duration",0.0)

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
                    "text":scene.text,

                    "keyword":scene.keyword,

                    "visuals":[

                        {

                            "prompt":v.prompt,

                            "duration":v.duration

                        }

                        for v in scene.visuals

                    ],

                    "duration":scene.duration
                }

                for scene in self.scenes

            ],

            "cta": self.cta,

        }