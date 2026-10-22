from app.generators import metadata_generator
from app.generators import script_generator
from app.image_styles import get_style
from app.schemas import Script
from app.schemas import YouTubeMetadata

SCRIPT = {
    "title": "Moon",
    "scenes": [
        {
            "text": "The Moon is leaving.",
            "keyword": "moon",
            "visuals": [{"prompt": "moon", "duration": 1.5}],
            "duration": 9.0,
        }
    ],
    "cta": "Follow for more.",
}


def test_script_generator_returns_validated_script(monkeypatch):
    captured = {}

    def fake_generate_json(prompt, schema):
        captured["prompt"] = prompt
        return schema.model_validate(SCRIPT)

    monkeypatch.setattr(script_generator, "generate_json", fake_generate_json)

    data = script_generator.generate_script("The Moon")

    assert Script.from_dict(data).scenes[0].duration == 0.0
    assert "The Moon" in captured["prompt"]


def test_metadata_tags_are_cleaned_not_padded(monkeypatch):
    def fake_generate_json(prompt, schema):
        return YouTubeMetadata(
            title="  Moon facts  ",
            description="About the Moon.",
            tags=["#moon", "Moon", "space", " ", "science"],
        )

    monkeypatch.setattr(metadata_generator, "generate_json", fake_generate_json)

    metadata = metadata_generator.generate_metadata(SCRIPT)

    assert metadata["title"] == "Moon facts"
    assert metadata["tags"] == ["moon", "space", "science"]


def test_style_lookup():
    assert "NASA concept art" in get_style("space")
    assert "\n" not in get_style("default")
