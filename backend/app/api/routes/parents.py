from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import (
    Parent,
    ParentCreate,
    ParentPublic,
    ParentPublicDetailed,
    ParentsPublic,
    ParentUpdate,
    Message,
    Kid,
)

router = APIRouter()


@router.get("/", response_model=ParentsPublic)
def read_parents(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve Parents.
    """
    count_statement = select(func.count()).select_from(Parent)
    count = session.exec(count_statement).one()
    statement = select(Parent).offset(skip).limit(limit)
    parents = session.exec(statement).all()

    return ParentsPublic(data=parents, count=count)


@router.get("/{id}", response_model=ParentPublicDetailed)
def read_parent(session: SessionDep, id: int) -> Any:
    """
    Get parent by ID.
    """
    parent = session.get(Parent, id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent


@router.post("/", response_model=ParentPublicDetailed)
def create_parent(*, session: SessionDep, parent_in: ParentCreate) -> Any:
    """
    Create new parent.
    """
    parent = Parent.model_validate(parent_in)
    session.add(parent)
    session.commit()
    session.refresh(parent)
    for kid_id in parent_in.kid_ids:
        db_kid = session.get(Kid, kid_id)
        if not db_kid:
            raise HTTPException(status_code=404, detail="Kid not found")
        parent.kids.append(db_kid)
    session.commit()
    session.refresh(parent)
    return parent


@router.put("/{id}", response_model=ParentPublic)
def update_parent(*, session: SessionDep, id: int, parent_in: ParentUpdate) -> Any:
    """
    Update a parent.
    """
    parent = session.get(Parent, id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    update_dict = parent_in.model_dump(exclude_unset=True)
    parent.sqlmodel_update(update_dict)
    session.add(parent)
    session.commit()
    session.refresh(parent)
    return parent


@router.delete("/{id}")
def delete_parent(session: SessionDep, id: int) -> Message:
    """
    Delete a parent.
    """
    parent = session.get(Parent, id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    session.delete(parent)
    session.commit()
    return Message(message="Parent deleted successfully")
