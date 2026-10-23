"""Photographic style blocks appended to every image prompt.

Buzzwords such as "8K, masterpiece, ray tracing, HDR, ultra realistic" push
image models toward a glossy CGI look. Real photographs are described by how
they were shot: camera, lens, light, film and imperfections. That is what
these styles describe, plus an explicit list of looks to avoid.
"""

AVOID = (
    "Avoid: CGI, 3D render, illustration, painting, cartoon, plastic or "
    "waxy skin, over-smoothed faces, oversaturated colors, heavy HDR glow, "
    "fantasy lighting, extra fingers, distorted hands, text, captions, "
    "logos, watermarks, borders."
)

DEFAULT_STYLE = f"""
Authentic documentary photograph, vertical 9:16 frame.
Shot on a full-frame camera with a 35mm lens at f/2.8, natural available light,
true-to-life colors, realistic skin pores and fabric texture, natural
imperfections, subtle film grain, slight depth of field, candid moment.
{AVOID}
"""

SPACE_STYLE = f"""
Real astronomy photograph, vertical 9:16 frame, as captured by a space
telescope or an astronaut camera aboard a spacecraft. Physically accurate
sunlight with hard shadows, black space with faint natural star field,
realistic surface detail, no lens flares, no glowing nebula clichés.
{AVOID}
"""

HISTORY_STYLE = f"""
Historically accurate documentary photograph, vertical 9:16 frame, as if taken
on location with a period-appropriate camera: correct clothing, materials,
architecture and tools for the era. Natural light, film grain, slightly faded
true-to-life colors (black and white for scenes before 1940), candid people.
{AVOID}
"""

SCIENCE_STYLE = f"""
Scientific documentary photograph, vertical 9:16 frame, real laboratory or
field setting. Macro or 50mm lens, accurate scale and materials, natural or
practical lab lighting, neutral color balance, crisp focus on the subject,
background softly out of focus.
{AVOID}
"""

TECH_STYLE = f"""
Editorial technology photograph, vertical 9:16 frame, real devices and real
places (offices, data centers, factories, streets). 35mm lens, practical light
sources such as screens and ceiling lights, believable reflections and
fingerprints, muted realistic color grade, subtle film grain.
{AVOID}
"""


STYLES = {
    "default": DEFAULT_STYLE,
    "space": SPACE_STYLE,
    "history": HISTORY_STYLE,
    "science": SCIENCE_STYLE,
    "tech": TECH_STYLE,
}


def get_style(name: str) -> str:
    """Style block by name (IMAGE_STYLE in .env), flattened to one line."""

    try:
        style = STYLES[name.strip().lower()]
    except KeyError:
        raise ValueError(
            f"Unknown IMAGE_STYLE {name!r}. Choose one of: {', '.join(STYLES)}"
        ) from None

    return " ".join(style.split())
