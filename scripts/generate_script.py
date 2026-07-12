import argparse

from app.services.script_service import run


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "id",
        type=int,
    )

    args = parser.parse_args()

    output = run(args.id)

    print(f"Script saved to: {output}")


if __name__ == "__main__":
    main()
