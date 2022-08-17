from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from superset import security_manager


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_position_id": partial(safe_proxy, self.current_user_position_id)
        }
        
    def current_user_position_id(self) -> Optional[str]:
        oidc = security_manager.oid
        info = oidc.user_getinfo(['preferred_username', 'given_name', 'family_name', 'email', 'positionId'])
        print(info)
        return info.get('positionId')