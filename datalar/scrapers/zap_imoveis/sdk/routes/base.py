from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, TYPE_CHECKING, TypedDict, Union, Optional

import httpx
from httpx._types import TimeoutTypes

if TYPE_CHECKING:
    from datalar.scrapers.zap_imoveis.sdk.sdk import ZapGlueAPI


class BaseHTTPError(Exception):
    """Classe base para erros HTTP personalizados."""

    pass


class NotFoundError(BaseHTTPError):
    """Classe para erros 404 - Recurso não encontrado."""

    ...


class Route(ABC):
    """
    Classe base para rotas da SDK do Zap Imóveis.
    Define a estrutura básica para rotas que interagem com a API.
    """

    def __init__(self, sdk: ZapGlueAPI) -> None:
        self.sdk = sdk

    @property
    @abstractmethod
    def resource_base_url(self) -> str:
        """
        URL base do recurso para a rota.
        """
        raise NotImplementedError("Subclasses must implement this property.")

    def raise_for_status(self, response: httpx.Response) -> None:
        """
        Verifica o status da resposta e levanta exceções apropriadas.

        :param response: A resposta HTTP a ser verificada.
        :raises NotFoundError: Se o status for 404.
        :raises BaseHTTPError: Para outros erros HTTP.
        """

        if not self.sdk.config.RAISE_FOR_STATUS:
            return

        try:
            if response.status_code not in (200, 201, 204):
                if response.status_code == 404:
                    raise NotFoundError(f"Resource not found: {response.url}")
                else:
                    raise BaseHTTPError(
                        f"HTTP error {response.status_code}: {response.text}"
                    )
        except httpx.HTTPError as e:
            self.log_error(e)
            self.sdk.logger.exception(e)
            raise BaseHTTPError(f"HTTP error occurred: {str(e)}")

    def build_url(self, *, resource_name: str = "") -> str:
        """
        Constrói a URL completa para o recurso especificado.

        :param resource_name: O nome do recurso para o qual a URL deve ser construída.
        :return: A URL completa do recurso.
        """
        if not resource_name.startswith("/") and resource_name:
            resource_name = f"/{resource_name}"
        if resource_name:
            return f"{self.sdk.BASE_URL}{self.resource_base_url}{resource_name}"
        return f"{self.sdk.BASE_URL}{self.resource_base_url}"

    def build_headers(self) -> Dict[str, str]:
        """
        Constrói os cabeçalhos HTTP para a requisição.

        :return: Um dicionário contendo os cabeçalhos HTTP.
        """

        H = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
            "Accept": "*/*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.zapimoveis.com.br/",
            "x-domain": ".zapimoveis.com.br",
            "X-DeviceId": "832cf7aa-c333-4ce3-9c95-9047ed90c642",
            "Origin": "https://www.zapimoveis.com.br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=4",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        return H

    def log_error(self, error: Exception) -> None:
        """
        Registra um erro no logger configurado.

        :param error: A exceção a ser registrada.
        """
        if self.sdk.logger.level(self.sdk.config.LOG_LEVEL) <= self.sdk.logger.level(
            "ERROR"
        ):
            self.sdk.logger.error(f"Error in {self.__class__.__name__}: {error}")

    def log_response(self, response: httpx.Response) -> None:
        """
        Registra a resposta HTTP no logger configurado.

        :param response: A resposta HTTP a ser registrada.
        """
        if self.sdk.config.LOG_RESPONSES and self.sdk.logger.level(
            self.sdk.config.LOG_LEVEL
        ) <= self.sdk.logger.level("DEBUG"):
            self.sdk.logger.debug(
                f"Response from {response.url} (status: {response.status_code}): {response.text}"
            )

    def log_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        data: Union[Dict[str, Any], None] = None,
    ) -> None:
        """
        Registra a requisição HTTP no logger configurado.

        :param method: O método HTTP da requisição (GET, POST, etc.).
        :param url: A URL da requisição.
        :param headers: Os cabeçalhos da requisição.
        :param data: Os dados da requisição (se houver).
        """
        if self.sdk.config.LOG_REQUESTS and self.sdk.logger.level(
            self.sdk.config.LOG_LEVEL
        ) <= self.sdk.logger.level("DEBUG"):
            self.sdk.logger.debug(
                f"Request {method} {url} - Headers: {headers} - Data: {data}"
            )

    def get(
        self,
        resource_name: str = "",
        params: Dict[str, Any] | None = None,
        timeout: Optional[TimeoutTypes] = None,
    ) -> httpx.Response:
        """
        Realiza uma requisição GET para o recurso especificado.

        :param resource_name: O nome do recurso para o qual a requisição deve ser feita.
        :param params: Parâmetros de consulta opcionais para a requisição.
        :param timeout: Tempo limite opcional para a requisição.
        :return: A resposta HTTP da requisição.
        """
        url = self.build_url(resource_name=resource_name)
        headers = self.build_headers()

        print(f"GET {url} with params: {params}")
        resp = httpx.get(
            url,
            headers=headers,
            params=params,
            timeout=timeout or self.sdk.config.DEFAULT_TIMEOUT,
        )
        print(resp.url)

        if self.sdk.config.LOG_REQUESTS:
            self.log_request("GET", url, headers, params)

        if self.sdk.config.RAISE_FOR_STATUS:
            self.raise_for_status(resp)

        if self.sdk.config.LOG_RESPONSES:
            self.log_response(resp)
        return resp
