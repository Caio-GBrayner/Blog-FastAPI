from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserRole, User
from app.models.post import Post
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_first_superuser(db: AsyncSession) -> None:
    user = await UserService.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            name="System",
            last_name="Administrator",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=UserRole.SUPER
        )
        await UserService.create(db, user_in=user_in)
        print(f"Initial superuser {settings.FIRST_SUPERUSER_EMAIL} created.")