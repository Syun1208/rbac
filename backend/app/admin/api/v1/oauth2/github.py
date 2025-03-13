#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi_limiter.depends import RateLimiter
from fastapi_oauth20 import FastAPIOAuth20, GitHubOAuth20
from starlette.responses import RedirectResponse

from backend.app.admin.conf import admin_settings
from backend.app.admin.service.oauth2_service import oauth2_service
from backend.common.enums import UserSocialType
from backend.common.response.response_schema import ResponseSchemaModel, response_base

router = APIRouter()

_github_client = GitHubOAuth20(admin_settings.OAUTH2_GITHUB_CLIENT_ID, admin_settings.OAUTH2_GITHUB_CLIENT_SECRET)
_github_oauth2 = FastAPIOAuth20(_github_client, admin_settings.OAUTH2_GITHUB_REDIRECT_URI)


@router.get('', summary='Get the Github authorization link')
async def github_auth2() -> ResponseSchemaModel[str]:
    auth_url = await _github_client.get_authorization_url(redirect_uri=admin_settings.OAUTH2_GITHUB_REDIRECT_URI)
    return response_base.success(data=auth_url)


@router.get(
    '/callback',
    summary='Github authorization automatic redirection',
    description='After Github authorization, it will automatically redirect to the current address and obtain user information, and automatically create a system user based on the user information',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def github_login(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    oauth2: FastAPIOAuth20 = Depends(_github_oauth2),
):
    token, _state = oauth2
    access_token = token['access_token']
    user = await _github_client.get_userinfo(access_token)
    data = await oauth2_service.create_with_login(
        request=request,
        response=response,
        background_tasks=background_tasks,
        user=user,
        social=UserSocialType.github,
    )
    return RedirectResponse(url=f'{admin_settings.OAUTH2_FRONTEND_REDIRECT_URI}?access_token={data.access_token}')
