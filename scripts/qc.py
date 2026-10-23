import argparse
import sys

from app.services.qc_service import run


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "id",
        type=int,
    )

    args = parser.parse_args()

    print()

    print("==============================")

    print("AI Content Factory QC")

    print("==============================")

    print()

    if not run(args.id):
        sys.exit(1)


if __name__ == "__main__":
    main()
