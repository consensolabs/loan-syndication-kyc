# -*- coding: utf-8 -*-

import falcon
from app.errors import UnauthorizedError, UnauthorizedUser, InvalidParameterError, UserRoleNotExistsError
from app.model import User, UserInfo


def auth_required(req, res, resource, params):

    if req.context["auth_user"] is None:
        raise UnauthorizedError()


def authorised_user(req, res, resource, params):

    auth_required(req, res, resource, params)
    try:
        user_db = User.find_by_sid(req.context["session"], req.context["auth_user"])
        if int(user_db.user_id) != int(req.context["data"]["user_id"]):
            raise UnauthorizedUser()
    except KeyError:
        raise InvalidParameterError(req.context["data"])

def admin_user(req, res, resource, params):

    auth_required(req, res, resource, params)
    user_db = User.find_by_sid(req.context["session"], req.context["auth_user"])

    # Verifying if the user has admin role
    try:
        if user_db.userroles[0].id != 1:
            raise UnauthorizedUser()
    except IndexError:
        raise UserRoleNotExistsError()
