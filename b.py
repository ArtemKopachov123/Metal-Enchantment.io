import bcrypt
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import re
import sqlite3

templates = Jinja2Templates("templates")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание базы данных (если ее еще нет)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )"""
)
conn.commit()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("Metal-Magic.html", {"request": request})

@app.get("/Metal-Magic", response_class=HTMLResponse)
async def read_root(request: Request):
  return templates.TemplateResponse("Metal-Magic.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
  return templates.TemplateResponse("login.html", {"request": request})

@app.get("/registration", response_class=HTMLResponse)
async def login(request: Request):
  return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/mm2", response_class=HTMLResponse)
async def welcome(request: Request, email: str = Form(...), password: str = Form(...)):
  # Валидация email
  if not re.match(
      r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email
  ):
    return JSONResponse({"error": "Неверный формат email"}, status_code=400)

  # Валидация пароля (например, минимум 8 символов)
  if len(password) < 8:
    return JSONResponse(
        {"error": "Пароль должен быть не менее 8 символов"},
        status_code=400,
    )
  
  if len(email) < 5:
    return JSONResponse(
        {"error": "Email должен быть не менее 5 символов"},
        status_code=400,
    )
  
  if len(email) > 32:
    return JSONResponse(
        {"error": "Email должен быть не более 32 символов"},
        status_code=400,
    )

  # Хэширование пароля
  hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

  # Сохранение хэшированного пароля в базу данных
  # cursor.execute(
  #     "INSERT INTO users (email, password) VALUES (?, ?)",
  #     (email, hashed_password.decode()),
  # )
  conn.commit()

  return templates.TemplateResponse(
      "mm2.html", {"request": request, "username": email}
  )

@app.get("/products", response_class=HTMLResponse)
async def products(request: Request):
  return templates.TemplateResponse("products.html", {"request": request})

@app.get("/contacts", response_class=HTMLResponse)
async def contact(request: Request):
  return templates.TemplateResponse("contacts.html", {"request": request})

# ... (Остальной код) ...