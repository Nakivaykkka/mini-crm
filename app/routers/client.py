from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


from app.database import get_db
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.models.client import Client
from app.core.dependencies import get_current_user
from app.models.user import User
from app.crud import client as crud

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.post("/", response_model=ClientRead)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = crud.create_client(db=db, client=client)
    return new_client

@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: UUID, db: Session = Depends(get_db)):
    client = crud.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/", response_model=List[ClientRead])
def get_all_clients(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    return crud.get_all_clients(db)

@router.patch("/{client_id}", response_model=ClientRead)
def update_client(
    client_id: UUID,
    update_data: ClientUpdate,
    db: Session = Depends(get_db)
    ):
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    update_fields = update_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(client, field, value)
        
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}")
def delete_client(client_id: UUID, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return Response(status_code=204)