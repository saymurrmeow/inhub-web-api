from collections.abc import Callable
from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.repositories.base import BaseRespository
from app.database.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(repo_type: Type[BaseRespository]) -> Callable[[Session], BaseRespository]:
    def _get_repo(db: Session = Depends(get_db)):
        return repo_type(db)

    return _get_repo
