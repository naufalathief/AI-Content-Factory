from pathlib import Path


def clean_srt(
    input_path: str,
    output_path: str,
) -> None:

    source = Path(input_path)

    if not source.exists():
        raise FileNotFoundError(source)

    cleaned_lines = []

    with open(
        source,
        "r",
        encoding="utf-8",
    ) as file:

        previous_blank = False

        for line in file:

            line = line.rstrip()

            if not line:

                if previous_blank:
                    continue

                previous_blank = True

            else:

                previous_blank = False

            cleaned_lines.append(line)

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline="\n",
    ) as file:

        file.write(
            "\n".join(cleaned_lines).strip()
        )
        file.write("\n")