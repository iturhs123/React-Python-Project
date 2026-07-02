from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
from models import Product
import database_models

app = FastAPI()
Base.metadata.create_all(bind=engine)

# CORS — allow React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return {"message": "Product added successfully"}

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for i in range(len(products)):
       if products[i].id == product_id:
           products[i] = product
           return {"message": "Product updated successfully"}
    return {"message": "No product found"}
    
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"message": "No product found"}
