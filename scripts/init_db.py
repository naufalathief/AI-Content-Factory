from app.database import engine
from app.database import Base

# Import semua model agar SQLAlchemy mengenali metadata
import app.models  # noqa: F401


def main():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")


if __name__ == "__main__":
    main()
