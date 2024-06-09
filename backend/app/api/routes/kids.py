from typing import Any
import logging

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import Kid, KidCreate, KidPublic, KidPublicDetailed, KidsPublic, KidUpdate, Message, Parent

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=KidsPublic)
def read_kids(
    session: SessionDep,  skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve Kids.
    """

    count_statement = select(func.count()).select_from(Kid)
    count = session.exec(count_statement).one()
    statement = select(Kid).offset(skip).limit(limit)
    kids = session.exec(statement).all()

    return KidsPublic(data=kids, count=count)


@router.get("/{id}", response_model=KidPublicDetailed)
def read_kid(session: SessionDep, id: int) -> Any:
    """
    Get kid by ID.
    """
    kid = session.get(Kid, id)
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    return kid


@router.post("/", response_model=KidPublicDetailed)
def create_kid(
    *, session: SessionDep, kid_in: KidCreate
) -> Any:
    """
    Create new kid.
    """
    kid = Kid.model_validate(kid_in)
    print(f"Creating kid {kid} with input data {kid_in}")
    session.add(kid)
    session.commit()
    session.refresh(kid)
    for parent_id in kid_in.parent_ids:
        db_parent = session.get(Parent, parent_id)
        print(f"Got parent {db_parent}, adding to Kid {kid}")
        if not db_parent:
            raise HTTPException(status_code=404, detail="Parent not found")
        kid.parents.append(db_parent)
    session.commit()
    session.refresh(kid)
    return kid


@router.put("/{id}", response_model=KidPublic)
def update_kid(
    *, session: SessionDep, id: int, kid_in: KidUpdate
) -> Any:
    """
    Update a kid.
    """
    kid = session.get(Kid, id)
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    update_dict = kid_in.model_dump(exclude_unset=True)
    kid.sqlmodel_update(update_dict)
    session.add(kid)
    session.commit()
    session.refresh(kid)
    return kid


@router.delete("/{id}")
def delete_kid(session: SessionDep, id: int) -> Message:
    """
    Delete a kid.
    """
    kid = session.get(Kid, id)
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    session.delete(kid)
    session.commit()
    return Message(message="Kid deleted successfully")
