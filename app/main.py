from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

DatabaseSession = Annotated[Session, Depends(get_db)]

app = FastAPI(title="Housing data")

@app.get("/")
def ausgabe():
    return "Herzlich Willkommen auf der Haus-Datenbank!"

@app.post("/houses", response_model=schemas.HouseOut, status_code=status.HTTP_201_CREATED)
def post_houses(request: schemas.HouseCreate, db: DatabaseSession):
    house = models.House(**request.model_dump())
    db.add(house)
    db.commit()
    db.refresh(house)
    return house

@app.get("/houses", response_model=list[schemas.HouseOut])
def get_all_houses(db: DatabaseSession):
    statement = select(models.House).order_by(models.House.id)
    return list(db.scalars(statement))

@app.get("/houses/{house_id}", response_model=schemas.HouseOut)
def get_information(house_id: int, db: DatabaseSession):
    statement = select(models.House).where(models.House.id == house_id)
    house = db.scalars(statement).first()
    if house is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    return house

@app.put("/houses/{house_id}", response_model=schemas.HouseOut)
def change_data_house(house_id: int, request: schemas.HouseCreate, db: DatabaseSession):
    statement = (
        update(models.House)
        .where(models.House.id == house_id)
        .values(**request.model_dump())
        .returning(models.House)
    )
    house = db.scalars(statement).first()
    if house is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    db.commit()
    db.refresh(house)
    return house

@app.delete("/houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id: int, db: DatabaseSession):
    statement = delete(models.House).where(models.House.id == house_id)
    result = db.execute(statement)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
    db.commit()