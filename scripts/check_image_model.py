from app.gemini_client import client


def main():
    model = client.models.get(
        model="models/gemini-2.5-flash-image"
    )

    print(model)


if __name__ == "__main__":
    main()