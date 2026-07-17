from fastapi import APIRouter, Request
from jose import jwt
from datetime import datetime, timedelta
from app.auth.google import oauth
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/google/login")
async def google_login(request: Request):

    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, "SECRET_KEY", algorithm="ALGORITHM")

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]
    print(user)

    return RedirectResponse("http://localhost:3000/Inventory")
