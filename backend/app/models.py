from sqlmodel import Field, Relationship, SQLModel
from app.other_models.default_models import *


class ParentKidLink(SQLModel, table=True):
    parent_id: int | None = Field(default=None, foreign_key="parent.id", primary_key=True)
    kid_id: int | None = Field(default=None, foreign_key="kid.id", primary_key=True)


# Shared properties
class ParentBase(SQLModel):
    name_and_surname: str
    email: str


# Database model, database table inferred from class name
class Parent(ParentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kids: list["Kid"] = Relationship(back_populates="parents", link_model=ParentKidLink)


# Properties to receive on item creation
class ParentCreate(ParentBase):
    kid_ids: list[int] | None = []


# Properties to return via API, id is always required
class ParentPublicDetailed(ParentBase):
    id: int
    kids: list["KidPublic"] | None = []


# Properties to return via API, id is always required
class ParentPublic(ParentBase):
    id: int


class ParentsPublic(SQLModel):
    data: list[ParentPublic]
    count: int


# Properties to receive on item update
class ParentUpdate(ParentBase):
    name_and_surname: str | None = None  # type: ignore
    email: str | None = None  # type: ignore


# Shared properties
class KidBase(SQLModel):
    name: str
    first_surname: str
    second_surname: str


# Database model, database table inferred from class name
class Kid(KidBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parents: list[Parent] = Relationship(back_populates="kids", link_model=ParentKidLink)


# Properties to receive on item creation
class KidCreate(KidBase):
    parent_ids: list[int] | None = []


# Properties to return via API, id is always required
class KidPublicDetailed(KidBase):
    id: int
    parents: list[ParentPublic] | None = []


# Properties to return via API, id is always required
class KidPublic(KidBase):
    id: int


class KidsPublic(SQLModel):
    data: list[KidPublic]
    count: int


# Properties to receive on item update
class KidUpdate(KidBase):
    name: str | None = None  # type: ignore
    first_surname: str | None = None  # type: ignore
    second_surname: str | None = None  # type: ignore
