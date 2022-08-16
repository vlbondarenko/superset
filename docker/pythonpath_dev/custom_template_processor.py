from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from flask import request
from flask_jwt_extended import decode_token


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_position_id": partial(safe_proxy, self.current_user_position_id)
        }
        
    def current_user_position_id(self) -> Optional[str]:
        access_token = request.cookies.get('oidc_id_token')
        print('OIDC ACCESS TOKEN ----------------------------------' + access_token)
        decodedToken = decode_token(access_token)
        print(decodedToken)
        print(decodedToken['email'])
        return 53