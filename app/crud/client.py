from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.core.security import get_password_hash


def cast_uuid(client_id):
    if not isinstance(client_id, UUID):
        try:
            client_id = UUID(str(client_id))
        except Exception as e:
            raise ValueError(f"UUID ERROR: {e}")
    return client_id



def create_client(db: Session, client: ClientCreate) -> Client:
    hashed_password = get_password_hash(client.password)
    new_client = Client(
        email=client.email,
        full_name=client.full_name,
        phone=client.phone,
        hashed_password=hashed_password
    )
    
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    return new_client


def get_client_by_id(db, client_id):
    client_id = cast_uuid(client_id)
    if isinstance(client_id, str):
        try:
            client_id = UUID(str(client_id))  
        except Exception as e:
            raise ValueError(f"UUID ERROR: {e}")

    return db.query(Client).filter(Client.id == client_id).first()

def get_all_clients(db: Session)-> list[Client]:
    return db.query(Client).all()

def update_client(
    db: Session,
    client_id: UUID,
    update_data: ClientUpdate
    ) -> Optional[Client]:
    
    client_id = cast_uuid(client_id)
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None
    
    update_fields = update_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: UUID) -> bool:
    client_id = cast_uuid(client_id)
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return False
    
    db.delete(client)
    db.commit()
    return True