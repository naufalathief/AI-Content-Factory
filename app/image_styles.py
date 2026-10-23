DEFAULT_STYLE = """
Ultra realistic,
photorealistic,
cinematic,
masterpiece,
8K,
HDR,
National Geographic quality,
volumetric lighting,
dramatic lighting,
global illumination,
ray tracing,
highly detailed,
sharp focus,
realistic textures,
depth of field,
professional photography,
vertical composition,
center subject,
no text,
no logo,
no watermark,
clean background
""".strip()


SPACE_STYLE = """
Ultra realistic,
cinematic,
NASA concept art,
deep space,
planetary lighting,
volumetric lighting,
photorealistic,
8K,
HDR,
highly detailed,
sharp focus,
vertical composition,
center subject,
no text,
no logo,
no watermark
""".strip()


HISTORY_STYLE = """
Ultra realistic,
historically accurate,
cinematic,
museum quality,
National Geographic,
photorealistic,
8K,
dramatic lighting,
highly detailed,
realistic textures,
vertical composition,
center subject,
no text,
no logo,
no watermark
""".strip()


SCIENCE_STYLE = """
Ultra realistic,
scientific visualization,
photorealistic,
cinematic,
8K,
National Geographic,
HDR,
volumetric lighting,
highly detailed,
sharp focus,
vertical composition,
center subject,
no text,
no logo,
no watermark
""".strip()


TECH_STYLE = """
Ultra realistic,
futuristic,
cyber technology,
photorealistic,
cinematic,
8K,
dramatic lighting,
highly detailed,
sharp focus,
vertical composition,
center subject,
no text,
no logo,
no watermark
""".strip()

STYLES = {
    "default": DEFAULT_STYLE,
    "space": SPACE_STYLE,
    "history": HISTORY_STYLE,
    "science": SCIENCE_STYLE,
    "tech": TECH_STYLE,
}


def get_style(name: str) -> str:
    """Style block by name (IMAGE_STYLE in .env)."""

    try:
        return STYLES[name.strip().lower()]
    except KeyError:
        raise ValueError(
            f"Unknown IMAGE_STYLE {name!r}. Choose one of: {', '.join(STYLES)}"
        ) from None
