import json
import os

import requests

from app.pexels_client import search_videos


MIN_DURATION = 2

MAX_DURATION = 15


def score_video(video):

    width = video["width"]
    height = video["height"]

    portrait = height > width

    duration = video["duration"]

    score = 0

    # Portrait lebih diutamakan
    if portrait:
        score += 1000

    # Video pendek lebih cocok Shorts
    if MIN_DURATION <= duration <= MAX_DURATION:
        score += 200

    # Resolusi tinggi
    score += width * height / 10000

    return score


def select_best_video(video):

    files = sorted(
        video["video_files"],
        key=lambda item: (
            item["width"] * item["height"],
            item.get("fps", 30),
        ),
        reverse=True,
    )

    return files[0]


def download_assets(
    video_id: int,
    keywords: list[str],
):

    folder = f"storage/assets/{video_id}"

    os.makedirs(
        folder,
        exist_ok=True,
    )

    metadata = []

    downloaded = set()

    counter = 1

    for keyword in keywords:

        result = search_videos(keyword)

        candidates = sorted(
            result["videos"],
            key=score_video,
            reverse=True,
        )

        downloaded_video = False

        for video in candidates:

            if video["id"] in downloaded:
                continue

            downloaded.add(video["id"])

            best = select_best_video(video)

            filename = f"{counter:03}.mp4"

            filepath = os.path.join(
                folder,
                filename,
            )

            print(
                f"Downloading: {keyword}"
            )

            response = requests.get(
                best["link"],
                timeout=60,
            )

            response.raise_for_status()

            with open(
                filepath,
                "wb",
            ) as file:

                file.write(
                    response.content
                )

            metadata.append(
                {
                    "file": filename,
                    "keyword": keyword,
                    "pexels_id": video["id"],
                    "duration": video["duration"],
                    "width": best["width"],
                    "height": best["height"],
                    "fps": best.get("fps"),
                }
            )

            counter += 1

            downloaded_video = True

            break

        if not downloaded_video:

            print(
                f"No video found: {keyword}"
            )

    with open(
        os.path.join(
            folder,
            "metadata.json",
        ),
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"\nDownloaded {len(metadata)} assets."
    )