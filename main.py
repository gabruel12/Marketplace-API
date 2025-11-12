from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(index=True)
    password: str = Field(index=True)

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: int = Field(index=True)
    obs: str | None = Field(default=None, index=True)
    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/user/cadaster/")
def cadasterUser(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/user/{user_id}/")
def userProfile(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@app.delete("/user/delete/{user_id}/")
def deleteUser(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not User:
        raise HTTPException(status_code=404, detail="User not found.")
    session.delete(user)
    session.commit()
    return {"ok": True}

@app.post("/product/create/")
def createProduct(product: Product, session: SessionDep) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/product/{product_id}/")
def listProducts(product_id: int, session: SessionDep) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@app.delete("/product/delete/{product_id}/")
def deleteProduct(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    session.delete(product)
    session.commit()
    return {"ok": True}