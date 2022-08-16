from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from flask import request
from flask_jwt_extended import jwt_required, current_user, get_current_user


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_position_id": partial(safe_proxy, self.current_user_position_id)
        }
        
    def current_user_position_id(self) -> Optional[str]:
        jwt_required()
        access_token = get_current_user()
        print('OIDC ACCESS TOKEN ----------------------------------' + access_token)
        return 53