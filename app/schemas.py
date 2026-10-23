"""Data contracts shared by Gemini, the generators and the renderer.

The same pydantic models are sent to Gemini as `response_schema`, so the
model can only answer with JSON in exactly this shape.
"""

from pydantic import BaseModel
from pydantic import Field


class Visual(BaseModel):

    prompt: str = Field(
        description="Cinematic image prompt for one visual moment.",
    )

    duration: float = Field(
        default=1.5,
        description="Relative weight of this visual inside its scene, 1.3-2.0.",
    )


class Scene(BaseModel):

    text: str = Field(
        description="One narrated sentence.",
    )

    keyword: str = Field(
        description="One SEO search keyword for this scene.",
    )

    visuals: list[Visual]

    # Spoken length of the scene, filled in from the voice timings.
    duration: float = 0.0


class Script(BaseModel):

    title: str

    scenes: list[Scene]

    cta: str

    @classmethod
    def from_dict(cls, data: dict) -> "Script":
        return cls.model_validate(data)

    def to_dict(self) -> dict:
        return self.model_dump()

    def narration(self) -> list[str]:
        """Every spoken block in order: the scenes, then the CTA."""
        return [scene.text for scene in self.scenes] + [self.cta]


class YouTubeMetadata(BaseModel):

    title: str = Field(
        description="YouTube title, at most 60 characters.",
    )

    description: str

    tags: list[str] = Field(
        description="Exactly 10 YouTube tags.",
    )
