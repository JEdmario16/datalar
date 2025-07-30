from __future__ import annotations

from dataclasses import dataclass

from typing import Literal, Optional, TYPE_CHECKING
from loguru._logger import Logger

if TYPE_CHECKING:
    from datalar.scrapers.zap_imoveis.sdk.routes.listings import Listings

@dataclass(init=True)
class SDKConfig:
    """
    Configurações para a SDK do Zap Imóveis.

    """
    LOG_REQUESTS: bool = False
    LOG_RESPONSES: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    DEFAULT_TIMEOUT: int = 10
    RAISE_FOR_STATUS: bool = True

    logger: Optional[Logger] = None

    def __post_init__(self):
        if not self.logger:
            import loguru
            import sys
            self.logger = loguru.logger
            self.logger.remove()
            self.logger.add(sys.stderr, level=self.LOG_LEVEL)

    

class ZapGlueAPI:
    BASE_URL: str = "https://glue-api.zapimoveis.com.br/v2/"
    def __init__(self, config: SDKConfig | None = None) -> None:
        self.config = config or SDKConfig()
        self.logger = self.config.logger

        # routes
        self._listings: Listings | None = None

    @property
    def listings(self) -> Listings:
        if not self._listings:
            from datalar.scrapers.zap_imoveis.sdk.routes.listings import Listings
            self._listings = Listings(self)
        return self._listings