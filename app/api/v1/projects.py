# -*- coding: utf-8 -*-

import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required, authorised_user, admin_user
from app.utils.auth import encrypt_token, hash_password, verify_password, uuid
from app.model import Projects, User
from app.errors import (
    AppError,
    InvalidParameterError,
    UserNotExistsError,
    PasswordNotMatch,
)

LOG = log.get_logger()


class Project(BaseResource):
    """
    Handle for endpoint: /v1/project
    """

    @falcon.before(admin_user)
    def on_post(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]

        if user_req:

            try:
                projectinfo_db = Projects.find_by_project_id(session=session, project_id=user_req.get("project_id"))
                projectinfo = projectinfo_db if projectinfo_db else Projects()
                projectinfo.user_id = user_req.get("user_id") if user_req.get("user_id") else projectinfo.user_id
                projectinfo.name = user_req.get("name") if user_req.get("name") else projectinfo.name
                projectinfo.p_revenue = user_req.get("revenue") if user_req.get("revenue") else projectinfo.p_revenue
                projectinfo.p_net_income = user_req.get("net_income") if user_req.get("net_income") else projectinfo.p_net_income
                projectinfo.p_total_assets = user_req.get("total_assets") if user_req.get("total_assets") else projectinfo.p_total_assets
                projectinfo.fund_source = user_req.get("fund_source") if user_req.get("fund_source") else projectinfo.fund_source

                session.add(projectinfo)
                self.on_success(res, None)
            except Exception as e:
                print(e)
                raise InvalidParameterError(req.context["data"])
        else:
            raise InvalidParameterError(req.context["data"])


    @falcon.before(admin_user)
    def on_get(self, req, res):
        session = req.context["session"]
        user_req = req.context["data"]

        try:
            if user_req.get("shared_id"):
                user_req['user_id'] = User.find_by_shared_id(session=session, id=user_req["shared_id"]).user_id

            projectinfo_db = Projects.find_by_user_id(session=session, user_id=user_req["user_id"])
            projectinfo = [project.to_dict() for project in projectinfo_db]

            self.on_success(res, projectinfo)
        except NoResultFound:
            raise UserNotExistsError("user id: %s" % user_req["user_id"])
