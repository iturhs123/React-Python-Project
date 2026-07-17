from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
from models import Product
import database_models
from app.routes.auth import router as auth_router
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
# CORS — allow React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001","http://localhost:3000/Inventory"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
Base.metadata.create_all(bind=engine)

products = [Product(id=1, name="Product A", price=10.99, description="Description of Product A", quantity=10),
            Product(id=2, name="Product B", price=19.99, description="Description of Product B", quantity=5)]

# ──────────────────────────────────
# JSON API Routes (for React frontend)
# ──────────────────────────────────

@app.get("/products")
def get_products():
    db = SessionLocal()
    try:
        return db.query(database_models.Product).all()
    finally:
        db.close()

@app.get("/products/{product_id}")
def get_productbyId(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"message": "Product not found"}

# @app.post("/products")
# def add_product(product: Product):
#     products.append(product)
#     return {"message": "Product added successfully"}
@app.post("/products")
def add_product(product: Product):
    db = SessionLocal()
    try:
        db_product = database_models.Product(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product
    finally:
        db.close()

# @app.put("/products/{product_id}")
# def update_product(product_id: int, product: Product):
#     for i in range(len(products)):
#        if products[i].id == product_id:
#            products[i] = product
#            return {"message": "Product updated successfully"}
#     return {"message": "No product found"}
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    db = SessionLocal()

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == product_id
    ).first()

    if not db_product:
        db.close()
        return {"message": "Product not found"}

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    db.close()

    return db_product
    
# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     for i in range(len(products)):
#         if products[i].id == product_id:
#             del products[i]
#             return {"message": "Product deleted successfully"}
#     return {"message": "No product found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == product_id
    ).first()

    if not db_product:
        db.close()
        return {"message": "Product not found"}

    db.delete(db_product)
    db.commit()
    db.close()

    return {"message": "Deleted successfully"}