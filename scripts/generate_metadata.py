import argparse

from app.services.metadata_service import run


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "id",
        type=int,
    )

    args = parser.parse_args()

    output = run(
        args.id,
    )

    print()

    print("Metadata generated.")

    print(output)


if __name__ == "__main__":
    main()
