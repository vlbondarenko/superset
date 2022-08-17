from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from flask import request
from flask_jwt_extended import decode_token, jwt_required, current_user, get_current_user
from flask_appbuilder.security.views import AuthOIDView
from customSecurity import OIDCSecurityManager
from flask import current_app as app
from flask_oidc import OpenIDConnect


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_position_id": partial(safe_proxy, self.current_user_position_id)
        }
        
    def current_user_position_id(self) -> Optional[str]:
        oidc = OpenIDConnect(app)
        info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'email', 'positionId'])
        print(oidc)
        print(info)
        access_token = request.cookies.get('oidc_id_token')
        print('OIDC ACCESS TOKEN ----------------------------------' + access_token)
        return 53