from fastapi import Header, HTTPException
from database import get_customer_by_api_key


async def require_api_key(x_api_key: str = Header(..., description="Your API key — get one at /auth/register")):
    customer = get_customer_by_api_key(x_api_key)
    if not customer:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    return customer