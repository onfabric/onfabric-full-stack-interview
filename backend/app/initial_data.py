import logging

from sqlalchemy.orm import Session

from app.core.db import Base, engine
from app.models import User

from app.core.config import settings
from app.models import ApiKey, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    Base.metadata.create_all(engine)

    user = session.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            fullname="Admin User",
            nickname="admin"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create initial API key for admin user
        api_key = ApiKey(
            key=settings.FIRST_SUPERUSER_KEY,
            user_id=user.id,
            name="Dashboard Key"
        )
        session.add(api_key)
        session.commit()

def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()