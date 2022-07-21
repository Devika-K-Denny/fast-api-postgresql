from cgi import print_exception
from fastapi import FastAPI,status,HTTPException,Request,Depends
from  pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import models


app=FastAPI()

templates=Jinja2Templates(directory="templates")

class Item(BaseModel):
    id:int
    name: str
    description:str
    price:int
    on_offer:bool

    class Config:
        orm_mode=True 
        
db=SessionLocal()

def get_db1():
    try:
        db1=SessionLocal()
        yield db1
    finally:
        db1.close()


@app.get("/")
def home(request: Request, db: Session= Depends(get_db1)):
    item_to_get=db.query(models.Item).all()
    print(item_to_get)
    return templates.TemplateResponse("home.html" , {
        "request": request,
        "item": item_to_get
    })

@app.post('/stock')
def create_stock():
    return {"Code": "Sucess",
            "Message": "Stock Created"
            }

@app.get('/items',response_model=List[Item],status_code=200)
def get_all_items():
    items=db.query(models.Item).all()
    return items

@app.get('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):
    db_item=db.query(models.Item).filter(models.Item.name==item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item already exists")

    item=db.query(models.Item).filter(models.Item.id==item_id).first()
    return item

@app.post('/items',response_model=Item,status_code=status.HTTP_201_CREATED)
def create_an_item(item:Item):
    new_item=models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )


    db.add(new_item)
    db.commit()

    return new_item

@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_an_item(item_id:int,item:Item):
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_update.name=item.name,
    item_to_update.price=item.price,
    item_to_update.description=item.description,
    item_to_update.on_offer=item.on_offer

    db.commit()

    return item_to_update

@app.delete('/item/{item_id}')
def delete_an_item(item_id:int):
    item_to_delete=db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource not found")
    
    db.delete(item_to_delete)
    db.commit()
    
    return item_to_delete

