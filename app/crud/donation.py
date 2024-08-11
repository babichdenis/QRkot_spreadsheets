from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase):

    async def create_donation(
            self,
            obj_in: DonationCreate,
            session: AsyncSession,
            user: User
    ) -> Donation:
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_user(
            self, session: AsyncSession, user: User
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
