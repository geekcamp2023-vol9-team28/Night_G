from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.timeline_posts_model import TimelinePostsModel
from typing import Optional


class TimelinePostsDAO:
    """Class for accessing timeline_posts table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_timeline_posts(self, user_id: int, content: str, image_url:  Optional[str]) -> None:
        new_timeline_posts = TimelinePostsModel(user_id=user_id, content=content, image_url=image_url)
        self.session.add(new_timeline_posts)
        await self.session.commit()

    async def get_timeline_posts(self, limit: int, offset: int) -> List[TimelinePostsModel]:
        raw_timeline = await self.session.execute(
            select(TimelinePostsModel).limit(limit).offset(offset),
        )

        return list(raw_timeline.scalars().fetchall())