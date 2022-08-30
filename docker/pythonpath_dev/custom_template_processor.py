from array import array
from functools import partial
from traceback import format_exc
from typing import Any, Iterable, List, Optional
from superset.jinja_context import JinjaTemplateProcessor, safe_proxy
from superset import security_manager


class CustomTemplateProcessor(JinjaTemplateProcessor):
    engine = "postgresql"

    def set_context(self, **kwargs: Any) -> None:
        super().set_context(**kwargs)
        self._context[self.engine] = {
            "current_user_distributor_id": partial(safe_proxy, self.current_user_distributor_id),
            "current_user_regions" : partial(safe_proxy,self.current_user_regions),
            "current_user_segments" : partial(safe_proxy,self.current_user_segments)
        }
        
    def current_user_distributor_id(self) -> Optional[str]:
        oidc = security_manager.oid
        info = oidc.user_getinfo(['distributorId'])
        return info.get('distributorId')
    
    def current_user_regions(self) -> List[str]:
        oidc = security_manager.oid
        info = oidc.user_getinfo(['regions'])
        regions = info.get('regions')
        strRegions = List[str]
        for region in regions:
            strRegions.insert(str(region), 0)
        return strRegions
    
    def current_user_segments(self) -> Iterable[int]:
        oidc = security_manager.oid
        info = oidc.user_getinfo(['segments'])
        return info.get('segments')