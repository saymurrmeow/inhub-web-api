from app.database.errors import EntityDoesNotExist
from app.database.repositories.base import BaseRespository
from app.database.orm.user import User
from app.models.schemas.user import UserInUpdate
from app.services import security


class UserRepository(BaseRespository):
    def get_by_email(self, *, email: str):
        user_row = self.connection.query(
            User).filter(User.email == email).first()

        if user_row:
            return user_row

        raise EntityDoesNotExist

    def get_by_username(self, *, username: str):
        user_row = self.connection.query(
            User).filter(User.username == username).first()

        if user_row:
            return user_row

        raise EntityDoesNotExist

    def create_new_user(self, *, username, email, password):
        db_user = User(username=username,
                       email=email,
                       hashed_password=security.get_password_hash(password))

        self.connection.add(db_user)
        self.connection.commit()
        self.connection.refresh(db_user)

        return db_user

    def update_user(self, *, user: UserInUpdate):
        db_user = self.connection.query(
            User).filter(User.username == user.username).first()

        db_user.username = user.username or db_user.username
        db_user.email = user.email or db_user.email
        db_user.is_mail_confirmed = user.is_mail_confirmed or db_user.is_mail_confirmed

        if user.password:
            db_user.hashed_password = security.get_password_hash(user.password)

        self.connection.add(db_user)
        self.connection.commit()
        self.connection.refresh(db_user)

        return db_user
