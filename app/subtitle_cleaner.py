import re


REPLACEMENTS = {
    " air ": " AI ",
    " Air ": " AI ",
    " ai ": " AI ",
    " reset ": " riset ",
    " Reset ": " Riset ",
    " open eye ": " OpenAI ",
    " Open Eye ": " OpenAI ",
    " cloud ": " Claude ",
    " Cloud ": " Claude ",
    " germany ": " Gemini ",
    " Germany ": " Gemini ",
}


def clean_text(text: str) -> str:
    text = f" {text} "

    for wrong, correct in REPLACEMENTS.items():
        text = text.replace(wrong, correct)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_srt(input_file: str, output_file: str):
    with open(
        input_file,
        "r",
        encoding="utf-8",
    ) as file:

        lines = file.readlines()

    cleaned = []

    for line in lines:

        if "-->" in line:
            cleaned.append(line)
            continue

        if line.strip().isdigit():
            cleaned.append(line)
            continue

        if line.strip() == "":
            cleaned.append(line)
            continue

        cleaned.append(
            clean_text(line) + "\n"
        )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        file.writelines(cleaned)
