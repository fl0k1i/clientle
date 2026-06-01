from fastapi import FastAPI, HTTPException, Path, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from schemas import SearchRequest, RegisterRequest, LoginRequest
from database import init_db, create_customer, get_customer_by_email
from auth import require_api_key
from client import c3_post, c3_get, close_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    await close_client()


app = FastAPI(title="Product Search API", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def http_error(e):
    if isinstance(e, PermissionError): return HTTPException(401, str(e))
    if isinstance(e, ValueError): return HTTPException(422, str(e))
    if isinstance(e, LookupError): return HTTPException(404, str(e))
    if isinstance(e, TimeoutError): return HTTPException(504, str(e))
    if isinstance(e, ConnectionError): return HTTPException(502, str(e))
    return HTTPException(500, str(e))


@app.get("/")
def landing():
    return FileResponse("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register")
def register(body: RegisterRequest):
    if len(body.password) < 8:
        raise HTTPException(422, "Password must be at least 8 characters")
    try:
        customer = create_customer(body.email, body.password)
    except ValueError as e:
        raise HTTPException(409, str(e))
    return {"message": "Account created", "email": customer["email"], "api_key": customer["api_key"]}


@app.post("/auth/login")
def login(body: LoginRequest):
    customer = get_customer_by_email(body.email, body.password)
    if not customer:
        raise HTTPException(401, "Invalid email or password")
    return {"email": customer["email"], "api_key": customer["api_key"]}


@app.post("/search")
async def search_products(body: SearchRequest, customer: dict = Depends(require_api_key)):
    if not any([body.query, body.image_url, body.base64_image]):
        raise HTTPException(422, "Provide at least one of: query, image_url, base64_image")
    try:
        return await c3_post("/v1/search", body.model_dump(exclude_none=True))
    except Exception as e:
        raise http_error(e)


@app.get("/products/{product_id}")
async def get_product(product_id: str = Path(...), website_ids: list[str] | None = Query(None), customer: dict = Depends(require_api_key)):
    params = {"website_ids": website_ids} if website_ids else None
    try:
        return await c3_get(f"/v1/products/{product_id}", params)
    except Exception as e:
        raise http_error(e)


@app.get("/products/{product_id}/similar")
async def similar_products(product_id: str = Path(...), customer: dict = Depends(require_api_key)):
    try:
        return await c3_get(f"/v1/products/{product_id}/similar")
    except Exception as e:
        raise http_error(e)


@app.get("/lookup")
async def lookup_product(url: str = Query(...), customer: dict = Depends(require_api_key)):
    try:
        return await c3_get("/v1/products/lookup", {"url": url})
    except Exception as e:
        raise http_error(e)