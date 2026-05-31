from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from schemas import SearchRequest
from client import c3_post, c3_get, close_client
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_client()


app = FastAPI(
    title="Channel3 Proxy",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def http_error(e: Exception) -> HTTPException:
    if isinstance(e, PermissionError):
        return HTTPException(401, str(e))
    if isinstance(e, ValueError):
        return HTTPException(422, str(e))
    if isinstance(e, LookupError):
        return HTTPException(404, str(e))
    if isinstance(e, TimeoutError):
        return HTTPException(504, str(e))
    if isinstance(e, ConnectionError):
        return HTTPException(502, str(e))
    return HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
async def search_products(body: SearchRequest):
    if not any([body.query, body.image_url, body.base64_image]):
        raise HTTPException(422, "Provide at least one of: query, image_url, base64_image")
    try:
        return await c3_post("/v1/search", body.model_dump(exclude_none=True))
    except Exception as e:
        raise http_error(e)


@app.get("/products/{product_id}")
async def get_product(
    product_id: str = Path(...),
    website_ids: list[str] | None = Query(None),
):
    params = {"website_ids": website_ids} if website_ids else None
    try:
        return await c3_get(f"/v1/products/{product_id}", params)
    except Exception as e:
        raise http_error(e)


@app.get("/products/{product_id}/similar")
async def similar_products(product_id: str = Path(...)):
    try:
        return await c3_get(f"/v1/products/{product_id}/similar")
    except Exception as e:
        raise http_error(e)


@app.get("/lookup")
async def lookup_product(url: str = Query(...)):
    try:
        return await c3_get("/v1/products/lookup", {"url": url})
    except Exception as e:
        raise http_error(e)