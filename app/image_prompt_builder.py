from app.image_styles import DEFAULT_STYLE


def build_prompt(
    content_prompt: str,
    style: str = DEFAULT_STYLE,
) -> str:

    return (
        f"{style}, "
        f"{content_prompt.strip()}"
    )