import os
from random import randint
import shutil
from typing import Annotated, Any
import uuid

from fastapi import APIRouter, BackgroundTasks, Body, Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authentication.auth import AuthService, get_current_user
from backend.authentication.utils import AuthUtils
from backend.database import get_async_session
from backend.models.msg_models import Msg, VerifyToken
from backend.services.user_img_upload import save_upload_cover
from backend.services.img_resize import resize_image

from ..models.auth_models import ResetPassword, Token, User, UserCreate, UserUpdate, UserUpdateImg, VerifyEmail, VerifyEmailToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-up", response_model=Token)
async def sign_up(user_data: UserCreate, service: AuthService = Depends()):
    return await service.registration_user(user_data)


@router.post("/sign-in", response_model=Token)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post("/verify-email-request", response_model=Token)
async def verify_user_email_request(email: VerifyEmail, service: AuthService = Depends()):
    result = await service.verify_email_request(email=email.email)
    return result


@router.post("/verify-user-email", response_model=Msg)
async def verify_user_email(
    token: VerifyEmailToken,
    service: AuthService = Depends(),
    db: AsyncSession = Depends(get_async_session),
    utils: AuthUtils = Depends(),
):
    user = await service.validate_veify_token(token=token.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    search_user = await utils.get_user_by_email(db=db, email=user.email)
    if not search_user:
        raise HTTPException(status_code=404, detail="User doesnt exist")
    
    await utils.verify_user_by_email(email=user.email, db=db)
    return {"msg": "Email verified successfully"}


@router.post("/recovery-password", response_model=Token)
async def recover_password(
    email: VerifyEmail,
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
):
    """
    Recovery password
    """
    result =  await service.recover_password(email=email.email)

    return result


@router.post("/reset-password", response_model=Msg)
async def reset_password(
    token: ResetPassword,
    db: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends(),
    utils: AuthUtils = Depends(),
) -> Any:
    """
    Reset password
    """
    user = await service.validate_recover_token(token=token.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    search_user = await utils.get_user_by_email(db=db, email=user.email)

    if not search_user:
        raise HTTPException(status_code=404, detail="User doesnt exist")

    hashed_password = await service.hash_password(token.password)
    await utils.add_new_password(email=user.email, new_password=hashed_password, db=db)
    return {"msg": "Password updated successfully"}


@router.patch("/update-user", response_model=Msg)
async def update_user_data(
    user_data: UserUpdate = Body(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await utils.update_user_data(email=user.email, db=db, user=user_data)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid Data")
    return {"msg": "Data updated successfully"}


@router.patch("/update-user-img", description='Обновление фото профиля, в базу сохраняется 200х200 картинка')
async def update_user_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    utils: AuthUtils = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    if not await utils.is_verified(user):
        raise HTTPException(status_code=400, detail="User not verified")
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!
    upload_dir = save_upload_cover(contents=contents, filename=file.filename, username=user.username)

    background_tasks.add_task(resize_image, filename=file.filename, path_file=upload_dir, db=db, user_id=user.user_id)
    return {"filename": file.filename}

