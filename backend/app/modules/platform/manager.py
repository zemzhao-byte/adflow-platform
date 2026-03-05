"""
平台Connector管理器

管理所有已绑定的广告平台账户和Connector实例。
提供统一的接口供上层业务调用。
"""
from __future__ import annotations

import time
import uuid
from typing import Optional
from dataclasses import dataclass, field

from .connectors.base import PlatformType, TokenInfo, BaseConnector, APIResult
from .connectors.meta import MetaConnector


@dataclass
class BoundAccount:
    """已绑定的平台账户"""
    bind_id: str
    platform: PlatformType
    name: str
    token: TokenInfo
    ad_accounts: list[dict] = field(default_factory=list)
    status: str = "active"
    created_at: float = 0.0
    last_synced_at: Optional[float] = None
    extra: dict = field(default_factory=dict)


class ConnectorManager:
    """单例管理器"""

    def __init__(self):
        self._bindings: dict[str, BoundAccount] = {}
        self._connectors: dict[str, BaseConnector] = {}

    def _create_connector(self, platform: PlatformType, token: TokenInfo) -> BaseConnector:
        if platform == PlatformType.META:
            return MetaConnector(token)
        raise ValueError(f"Platform {platform} not supported yet")

    async def bind_platform(self, platform: PlatformType, token_str: str,
                            name: Optional[str] = None) -> dict:
        """绑定一个新的平台账户"""
        token = TokenInfo(access_token=token_str)
        connector = self._create_connector(platform, token)

        validate_result = await connector.validate_token()
        if not validate_result.success:
            return {"success": False, "error": validate_result.error_message}

        accounts_result = await connector.get_ad_accounts()
        ad_accounts = accounts_result.data if accounts_result.success else []

        bind_id = str(uuid.uuid4())[:8]
        binding = BoundAccount(
            bind_id=bind_id,
            platform=platform,
            name=name or f"{platform.value.title()} Account",
            token=token,
            ad_accounts=ad_accounts,
            created_at=time.time(),
            extra={"user_info": validate_result.data},
        )
        self._bindings[bind_id] = binding
        self._connectors[bind_id] = connector

        return {
            "success": True,
            "bind_id": bind_id,
            "platform": platform.value,
            "name": binding.name,
            "ad_accounts": ad_accounts,
            "user_info": validate_result.data,
        }

    def unbind_platform(self, bind_id: str) -> bool:
        if bind_id in self._bindings:
            del self._bindings[bind_id]
            self._connectors.pop(bind_id, None)
            return True
        return False

    def update_binding(self, bind_id: str, name: str | None = None,
                       status: str | None = None) -> dict | None:
        b = self._bindings.get(bind_id)
        if not b:
            return None
        if name is not None:
            b.name = name
        if status is not None:
            b.status = status
        return self._binding_to_dict(b)

    async def update_token(self, bind_id: str, new_token: str) -> dict:
        b = self._bindings.get(bind_id)
        if not b:
            return {"success": False, "error": "Binding not found"}
        token = TokenInfo(access_token=new_token)
        connector = self._create_connector(b.platform, token)
        result = await connector.validate_token()
        if not result.success:
            return {"success": False, "error": result.error_message}
        b.token = token
        self._connectors[bind_id] = connector
        accts = await connector.get_ad_accounts()
        if accts.success:
            b.ad_accounts = accts.data
            b.last_synced_at = time.time()
        return {"success": True, "ad_accounts": b.ad_accounts}

    def get_binding_detail(self, bind_id: str) -> dict | None:
        b = self._bindings.get(bind_id)
        if not b:
            return None
        d = self._binding_to_dict(b)
        d["token_preview"] = b.token.access_token[:8] + "..." + b.token.access_token[-4:] if len(b.token.access_token) > 12 else "****"
        d["user_info"] = b.extra.get("user_info", {})
        return d

    def _binding_to_dict(self, b: BoundAccount) -> dict:
        return {
            "bind_id": b.bind_id,
            "platform": b.platform.value,
            "name": b.name,
            "status": b.status,
            "ad_accounts_count": len(b.ad_accounts),
            "ad_accounts": b.ad_accounts,
            "created_at": b.created_at,
            "last_synced_at": b.last_synced_at,
        }

    def list_bindings(self) -> list[dict]:
        return [self._binding_to_dict(b) for b in self._bindings.values()]

    def get_connector(self, bind_id: str) -> Optional[BaseConnector]:
        return self._connectors.get(bind_id)

    def get_binding(self, bind_id: str) -> Optional[BoundAccount]:
        return self._bindings.get(bind_id)

    def find_connector_by_account(self, account_id: str) -> Optional[tuple[str, BaseConnector]]:
        """通过广告账户ID查找对应的Connector"""
        for bind_id, binding in self._bindings.items():
            for acct in binding.ad_accounts:
                if acct.get("id") == account_id:
                    return bind_id, self._connectors[bind_id]
        return None

    async def sync_accounts(self, bind_id: str) -> dict:
        """重新同步广告账户列表"""
        connector = self._connectors.get(bind_id)
        binding = self._bindings.get(bind_id)
        if not connector or not binding:
            return {"success": False, "error": "Binding not found"}
        result = await connector.get_ad_accounts()
        if result.success:
            binding.ad_accounts = result.data
            binding.last_synced_at = time.time()
        return {"success": result.success, "ad_accounts": result.data if result.success else []}


manager = ConnectorManager()


async def seed_demo_data():
    """设计阶段自动注入Demo绑定，方便体验完整功能流程"""
    if manager._bindings:
        return
    await manager.bind_platform(
        PlatformType.META,
        "DEMO_TOKEN_meta_growth_team",
        "Growth Team - Meta (Demo)"
    )
