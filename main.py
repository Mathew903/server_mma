from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, get_db
from datetime import datetime
from sqlalchemy.orm import Session
import models

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    id: int | None = None
    name: str
    password: str
    rol: int
    creado: datetime | None = None

class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: float
    creado_por: int
    fecha_creacion: datetime | None = None

app = FastAPI()
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root_get():
    return {"message": "hola mundo"}

@app.post("/login/")
async def login(user: User):
    return User(name=user.name, password = user.password)

@app.get("/users/", status_code=200)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User)
    return users

@app.post("/registrar/", status_code=201)
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, password=user.password, rol=user.rol) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User(name=db_user.name, id=db_user.id, password=db_user.password, rol=db_user.rol, creado=db_user.creado)

@app.get("/products/{user_id}", status_code=200)
async def get_products_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Producto).filter(models.Producto.creado_por == user_id).all()

@app.post("/create-product/", status_code=201)
async def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = models.Producto(name=product.name, description=product.description, price=product.price, creado_por=product.creado_por) 
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return Product(
        id= db_product.id, 
        name= db_product.name, 
        description= db_product.description, 
        creado_por= db_product.creado_por, 
        price= db_product.price, 
        fecha_creacion=db_product.fecha_creacion
    )

