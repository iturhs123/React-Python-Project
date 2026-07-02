from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from models import Product

app = FastAPI()

# CORS — allow React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 template configuration
templates = Jinja2Templates(directory="templates")

# Serve static files (images, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

products = [Product(id=1, name="Product A", price=10.99, description="Description of Product A", quantity=10),
            Product(id=2, name="Product B", price=19.99, description="Description of Product B", quantity=5)]

# ──────────────────────────────────────────────
# Jinja2 Template Routes (Server-Side Rendered)
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html",
        context={"products": products, "product_count": len(products)},
    )

@app.get("/products-page", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="products.html",
        context={"products": products},
    )

@app.get("/add-product-page", response_class=HTMLResponse)
def add_product_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="add_product.html",
    )

@app.get("/payroll-notification", response_class=HTMLResponse)
def payroll_notification(request: Request):
    return templates.TemplateResponse(
        request=request, name="payroll_notification.html",
        context={
            "banner_image_url": "/static/images/Email_hero_image.jpg",
            "date": "April 8, 2026",
            "application_link": "#",
            "user_name": "John Doe",
            "modified_entries": 5,
            "pending_notifications": 3,
            "text1": "Info A",
            "text2": "Info B",
            "text3": "Info C",
            "text4": "Info D",
            "year": 2026,
        },
    )

# @app.post("/add-product-page", response_class=HTMLResponse)
# def add_product_form(
#     request: Request,
#     id: int = Form(...),
#     name: str = Form(...),
#     description: str = Form(...),
#     price: float = Form(...),
#     quantity: int = Form(...),
# ):
#     product = Product(id=id, name=name, price=price, description=description, quantity=quantity)
#     products.append(product)
#     return templates.TemplateResponse(
#         request=request, name="payroll_notification.html",
#         context={"payroll_notification": products, "message": "Product added successfully!"},
#     )

@app.get("/edit-product-page/{product_id}", response_class=HTMLResponse)
def edit_product_page(request: Request, product_id: int):
    for product in products:
        if product.id == product_id:
            return templates.TemplateResponse(
                request=request, name="edit_product.html",
                context={"product": product},
            )
    return templates.TemplateResponse(
        request=request, name="products.html",
        context={"products": products, "error": "Product not found"},
    )

@app.post("/edit-product-page/{product_id}", response_class=HTMLResponse)
def edit_product_form(
    request: Request,
    product_id: int,
    id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
):
    for i in range(len(products)):
        if products[i].id == product_id:
            products[i] = Product(id=id, name=name, price=price, description=description, quantity=quantity)
            return templates.TemplateResponse(
                request=request, name="products.html",
                context={"products": products, "message": "Product updated successfully!"},
            )
    return templates.TemplateResponse(
        request=request, name="products.html",
        context={"products": products, "error": "Product not found"},
    )

@app.post("/delete-product/{product_id}")
def delete_product_form(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            del products[i]
            return RedirectResponse(url="/products-page", status_code=303)
    return RedirectResponse(url="/products-page", status_code=303)

# ──────────────────────────────────
# JSON API Routes (for React frontend)
# ──────────────────────────────────

@app.get("/api/products")
def get_products():
    return products

@app.get("/api/products/{product_id}")
def get_productbyId(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"message": "Product not found"}

@app.post("/api/products")
def add_product(product: Product):
    products.append(product)
    return {"message": "Product added successfully"}

@app.put("/api/products/{product_id}")
def update_product(product_id: int, product: Product):
    for i in range(len(products)):
       if products[i].id == product_id:
           products[i] = product
           return {"message": "Product updated successfully"}
    return {"message": "No product found"}
    
@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"message": "No product found"}
