#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.sys.config import router as config_router
from backend.app.admin.api.v1.sys.data_rule import router as data_rule_router
from backend.app.admin.api.v1.sys.dept import router as dept_router
from backend.app.admin.api.v1.sys.dict_data import router as dict_data_router
from backend.app.admin.api.v1.sys.dict_type import router as dict_type_router
from backend.app.admin.api.v1.sys.menu import router as menu_router
from backend.app.admin.api.v1.sys.plugin import router as plugin_router
from backend.app.admin.api.v1.sys.role import router as role_router
from backend.app.admin.api.v1.sys.token import router as token_router
from backend.app.admin.api.v1.sys.upload import router as upload_router
from backend.app.admin.api.v1.sys.user import router as user_router

router = APIRouter(prefix='/sys')

router.include_router(config_router, prefix='/configs', tags=['System Configuration'])
router.include_router(dept_router, prefix='/depts', tags=['System Department'])
router.include_router(dict_data_router, prefix='/dict-datas', tags=['System dictionary data'])
router.include_router(dict_type_router, prefix='/dict-types', tags=['System dictionary type'])
router.include_router(menu_router, prefix='/menus', tags=['System Menu'])
router.include_router(role_router, prefix='/roles', tags=['System Roles'])
router.include_router(user_router, prefix='/users', tags=['System Users'])
router.include_router(data_rule_router, prefix='/data-rules', tags=['System data permission rules'])
router.include_router(token_router, prefix='/tokens', tags=['System Token'])
router.include_router(upload_router, prefix='/upload', tags=['System upload'])
router.include_router(plugin_router, prefix='/plugin', tags=['System plugins'])
