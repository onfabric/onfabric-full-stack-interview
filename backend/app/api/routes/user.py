from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schema
from app.deps import get_db, get_user_from_key
from app.models import User

router = APIRouter(prefix="/user")

@router.get(
    "",
    response_model=schema.User,
    summary="Get Current User",
    description="Returns the currently authenticated user's profile information including email, name and nickname.",
    response_description="The current user's profile data"
)
def read_user(
    current_user: User = Depends(get_user_from_key),
):
    return current_user

@router.put(
    "",
    response_model=schema.User,
    summary="Update Current User",
    description="Updates the currently authenticated user's profile information. All fields are optional and only provided fields will be updated.",
    response_description="The updated user profile",
    responses={404: {"description": "User not found"}}
)
def update_user(
    user: schema.UserCreate,
    current_user: User = Depends(get_user_from_key),
    db: Session = Depends(get_db)
):
    db_user = crud.user_put(db=db, user_id=current_user.id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get(
    "/keys",
    response_model=List[schema.ApiKey],
    summary="List User's API Keys",
    description="Returns a paginated list of API keys belonging to the current user. Each key includes its ID, name and creation timestamp.",
    response_description="List of user's API keys and the total key count"
)
def read_user_keys(
    current_user: User = Depends(get_user_from_key),
    db: Session = Depends(get_db)
):
    return crud.user_keys_get(db=db, user_id=current_user.id)

@router.post(
    "/keys",
    response_model=schema.ApiKey,
    summary="Create New API Key",
    description="Creates a new API key for the current user. Requires a name for the key. The actual key value is automatically generated.",
    response_description="The newly created API key"
)
def create_user_key(
    key: schema.ApiKeyCreate,
    current_user: User = Depends(get_user_from_key),
    db: Session = Depends(get_db)
):
    return crud.user_key_post(db=db, key=key, user_id=current_user.id)

@router.get(
    "/keys/{key_id}",
    response_model=schema.ApiKey,
    summary="Get Specific API Key",
    description="Retrieves details about a specific API key by its ID. Only returns keys belonging to the current user.",
    response_description="The requested API key details",
    responses={404: {"description": "API key not found"}}
)
def read_user_key(
    key_id: str,
    current_user: User = Depends(get_user_from_key),
    db: Session = Depends(get_db)
):
    db_key = crud.user_key_get(db=db, user_id=current_user.id, key_id=key_id)
    if db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_key

@router.delete(
    "/keys/{key_id}",
    response_model=schema.ApiKey,
    summary="Delete API Key",
    description="Deletes a specific API key by its ID. This action cannot be undone.",
    response_description="The deleted API key",
    responses={404: {"description": "API key not found"}}
)
def delete_user_key(
    key_id: str,
    db: Session = Depends(get_db)
):
    db_key = crud.user_key_delete(db=db, key_id=key_id)
    if db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_key

@router.get(
    "/keys/{key_id}/requests",
    response_model=List[schema.UserRequest],
    summary="List API Key Usage History",
    description="Returns a paginated list of requests made using a specific API key. Includes endpoint, method, status code and timestamp for each request.",
    response_description="List of API requests made with the specified key and the total amount of requests"
)
def read_user_requests(
    key_id: str,
    current_user: User = Depends(get_user_from_key),
    db: Session = Depends(get_db)
):
    return crud.user_requests_get(db=db, user_id=current_user.id, key_id=key_id)


@router.get(
    "/requests/{request_id}",
    response_model=schema.UserRequest,
    summary="Get Specific Request Details",
    description="Retrieves detailed information about a specific API request by its ID.",
    response_description="The requested API request details",
    responses={404: {"description": "Request not found"}}
)
def read_user_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    db_request = crud.user_request_get(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.delete(
    "/requests/{request_id}",
    response_model=schema.UserRequest,
    summary="Delete Request Record",
    description="Deletes a specific request record by its ID. This action cannot be undone.",
    response_description="The deleted request record",
    responses={404: {"description": "Request not found"}}
)
def delete_user_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    db_request = crud.user_request_delete(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request
