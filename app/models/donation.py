from sqlalchemy import Column, Integer, Text, ForeignKey

from .common_base import CommonBase


class Donation(CommonBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{super().__repr__()},'
            f'user_id={self.user_id},'
            f'comment={self.comment}'
        )
