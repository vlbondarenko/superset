from functools import partial
from typing import Any, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from superset import security_manager


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context.update(
            {
                "current_user_distributor_id": partial(safe_proxy, self.current_user_distributor_id),
                "current_user_regions": partial(safe_proxy, self.current_user_regions),
                "current_user_segments": partial(safe_proxy, self.current_user_segments)
            })

    def current_user_distributor_id(self) -> Optional[str]:
        oidc = security_manager.oid
        info = oidc.user_getinfo(['distributorId'])
        return info.get('distributorId')

    def current_user_regions(self):
        oidc = security_manager.oid
        info = oidc.user_getinfo(['regions'])
        regions = info.get('regions')
        return [str(region) for region in regions]

    def current_user_segments(self):
        oidc = security_manager.oid
        info = oidc.user_getinfo(['segments'])
        segments = info.get('segments')
        return [str(segment) for segment in segments]