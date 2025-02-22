from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from models.userModel import *
from config.db import conn
from security.jwt import *
from fastapi.responses import JSONResponse



user = APIRouter()
templates = Jinja2Templates(directory="templates")



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = conn.nmsapp.user.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user



@user.post("/register")
async def register(user: User):

    if user.role not in ["temp", "admin"]:
        return {"message": "Invalid role. Role must be either 'temp' or 'admin'."}

    if conn.nmsapp.user.find_one({"username": user.username}):
        return {"message": "Username already exists."}

    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    conn.nmsapp.user.insert_one(user_dict)
    return {"message": "User registered successfully"}

@user.post("/login")
async def login(usera: UserLogin):
    db_user = conn.nmsapp.user.find_one({"username": usera.username})
    if not db_user or not verify_password(usera.password, db_user["password"]):
        return {"message": "Incorrect username or password"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": usera.username, "role": db_user["role"]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": usera.username}, expires_delta=refresh_token_expires
    )
    return {"access": access_token, "refresh": refresh_token,"username": usera.username ,"role": db_user["role"]}

@user.post("/refresh")
async def refresh_token(refresh_token: RefreshTokenRequest):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token.refresh, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = conn.nmsapp.user.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return {"access": access_token, "token": "bearer"}

@user.get("/dashboard")
async def admin_only(current_user: dict = Depends(get_current_user)):
    current_user.pop("_id")
    if current_user["role"] != "admin":
        return {"message": "You do not have permission to access this resource."}
    return JSONResponse(content=current_user, status_code=status.HTTP_200_OK)
    # return {"message": "Welcome, admin!"}