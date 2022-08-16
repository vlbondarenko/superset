from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from flask import request


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_position_id": partial(safe_proxy, self.current_user_position_id)
        }
        
    def current_user_position_id(self) -> Optional[str]:
        access_token = request.cookies.get('session')
        print(access_token)
        return 53