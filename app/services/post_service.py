from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post, PostStatus
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    @staticmethod
    async def create(
        db: AsyncSession,
        post_in: PostCreate,
        author_id: UUID
    ) -> Post:
        post = Post(
            title=post_in.title,
            content=post_in.content,
            excerpt=post_in.excerpt,
            author_id=author_id,
            status=PostStatus.DRAFT
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        post_id: UUID,
        include_draft: bool = False
    ) -> Optional[Post]:
        query = select(Post).where(Post.id == post_id)
        if not include_draft:
            query = query.where(Post.status == PostStatus.PUBLISHED)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        status: str = "published"
    ) -> tuple:
        query = select(Post)
        
        if status == "published":
            query = query.where(Post.status == PostStatus.PUBLISHED)
        
        query = query.order_by(desc(Post.created_at))
        
        count_query = select(func.count(Post.id))
        if status == "published":
            count_query = count_query.where(Post.status == PostStatus.PUBLISHED)
        
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        posts = result.scalars().all()
        
        return posts, total

    @staticmethod
    async def update(
        db: AsyncSession,
        post_id: UUID,
        post_update: PostUpdate,
        current_user: User
    ) -> Optional[Post]:
        post = await PostService.get_by_id(db, post_id, include_draft=True)
        
        if not post:
            return None
        
        if post.author_id != current_user.id and current_user.role.value != "SUPER":
            return None
        
        for field, value in post_update.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(post, field, value)
        
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def delete(
        db: AsyncSession,
        post_id: UUID,
        current_user: User
    ) -> bool:
        if current_user.role.value != "SUPER":
            return False
        
        post = await PostService.get_by_id(db, post_id, include_draft=True)
        
        if not post:
            return False
        
        await db.delete(post)
        await db.commit()
        return True
