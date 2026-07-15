from app.gemini_client import client


def main():

    for model in client.models.list():

        if model.name == "models/gemini-2.5-flash-image":

            print(model)


if __name__ == "__main__":

    main()