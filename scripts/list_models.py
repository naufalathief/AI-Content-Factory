from app.providers.gemini_client import MODEL_IMAGE, get_client


def main():

    for model in get_client().models.list():

        if model.name == f"models/{MODEL_IMAGE}":

            print(model)


if __name__ == "__main__":

    main()