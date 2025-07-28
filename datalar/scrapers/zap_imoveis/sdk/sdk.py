from dataclasses import dataclass

from typing import Literal, Optional
from loguru._logger import Logger

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