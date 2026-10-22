from app.providers.gemini_client import MODEL_IMAGE, get_client


def main():
    model = get_client().models.get(
        model=f"models/{MODEL_IMAGE}"
    )

    print(model)


if __name__ == "__main__":
    main()