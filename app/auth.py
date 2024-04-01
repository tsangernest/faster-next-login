from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
#     user = fake_decode_token(token=token)
#
#     if not user:app
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Invalid login credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     return user


