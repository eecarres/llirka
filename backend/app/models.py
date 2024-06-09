from sqlmodel import Field, Relationship, SQLModel


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


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str
