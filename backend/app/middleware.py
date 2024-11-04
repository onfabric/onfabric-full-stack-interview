from fastapi import Request
from app.core.db import SessionLocal
from app import models


async def api_request_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Only track requests with API keys
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return response

    # Get DB session
    db = SessionLocal()
    try:
        # Find the API key record
        key = db.query(models.ApiKey).filter(models.ApiKey.key == api_key).first()
        if key:
            # Create request record
            request_record = models.UserRequest(
                key_id=key.id,
                endpoint=str(request.url.path),
                method=request.method,
                status_code=response.status_code
            )
            db.add(request_record)
            db.commit()
    finally:
        db.close()

    return response

