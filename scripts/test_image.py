from app.gemini_image_provider import generate_image


def main():

    generate_image(
        prompt="""
A gigantic futuristic O'Neill Cylinder orbiting Earth.

Ultra realistic.

Photorealistic.

Cinematic.

8K.

National Geographic documentary.

Vertical composition.

No text.

No logo.

No watermark.
""",
        output_path="storage/test.png",
    )

    print("Done.")


if __name__ == "__main__":

    main()