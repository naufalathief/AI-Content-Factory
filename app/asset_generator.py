import json
import os

import requests

from app.pexels_client import search_videos


def select_best_video(video_files):
    return sorted(
        video_files,
        key=lambda item: (
            item["width"],
            item["height"],
            item.get("fps", 30),
        ),
        reverse=True,
    )[0]


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

        for video in result["videos"]:

            if video["id"] in downloaded:
                continue

            downloaded.add(video["id"])

            best = select_best_video(
                video["video_files"],
            )

            filename = f"{counter:03}.mp4"

            filepath = os.path.join(
                folder,
                filename,
            )

            response = requests.get(
                best["link"],
                timeout=60,
            )

            with open(
                filepath,
                "wb",
            ) as file:
                file.write(response.content)

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

            break

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
