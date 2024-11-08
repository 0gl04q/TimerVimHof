from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base, int_pk, int_positive
from app.users.models import User


class TrainingProfile(Base):
    id: Mapped[int_pk]
    name: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='training_profiles')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name}, user_id={self.user_id})'

    def __repr__(self):
        return str(self)


class BreathingCycle(Base):
    id: Mapped[int_pk]
    duration: Mapped[int_positive]

    training_profile_id: Mapped[int] = mapped_column(ForeignKey('trainingprofiles.id'), nullable=False)
    training_profile: Mapped['TrainingProfile'] = relationship('TrainingProfile', back_populates='breathing_cycle')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, duration={self.duration}, training_profile_id={self.training_profile_id})'

    def __repr__(self):
        return str(self)
