from unittest.mock import MagicMock

import pytest

from datalar.scrapers.zap_imoveis.sdk.sdk import SDKConfig, ZapGlueAPI


# Fixture para a configuração customizada
@pytest.fixture
def custom_config() -> SDKConfig:
    """Retorna uma instância de SDKConfig com valores não-padrão."""
    return SDKConfig(
        LOG_LEVEL="WARNING",
        LOG_REQUESTS=True,
        LOG_RESPONSES=True,
        DEFAULT_TIMEOUT=5,
        RAISE_FOR_STATUS=False,
    )


# Teste parametrizado que substitui os dois testes iniciais
@pytest.mark.parametrize(
    "config, expected_values",
    [
        # Caso 1: Teste com a configuração padrão (config=None)
        (
            None,
            {
                "LOG_LEVEL": "INFO",
                "LOG_REQUESTS": False,
                "LOG_RESPONSES": False,
                "DEFAULT_TIMEOUT": 10,
                "RAISE_FOR_STATUS": True,
            },
        ),
        # Caso 2: Teste com a configuração customizada
        (
            "custom_config",  # Pytest irá injetar a fixture aqui
            {
                "LOG_LEVEL": "WARNING",
                "LOG_REQUESTS": True,
                "LOG_RESPONSES": True,
                "DEFAULT_TIMEOUT": 5,
                "RAISE_FOR_STATUS": False,
            },
        ),
    ],
)
def test_sdk_initialization(config, expected_values, request):
    """
    Testa a inicialização da SDK com diferentes configurações (padrão e customizada).
    """
    # 1. Preparação:
    # Pytest resolve a string "custom_config" e injeta o resultado da fixture
    if isinstance(config, str):
        config = request.getfixturevalue(config)

    # 2. Execução:
    sdk = ZapGlueAPI(config=config)

    # 3. Verificação:
    assert sdk.logger is not None
    assert sdk.config.LOG_LEVEL == expected_values["LOG_LEVEL"]
    assert sdk.config.LOG_REQUESTS == expected_values["LOG_REQUESTS"]
    assert sdk.config.LOG_RESPONSES == expected_values["LOG_RESPONSES"]
    assert sdk.config.DEFAULT_TIMEOUT == expected_values["DEFAULT_TIMEOUT"]
    assert sdk.config.RAISE_FOR_STATUS == expected_values["RAISE_FOR_STATUS"]


def test_sdk_config_post_init_creates_logger():
    """
    Testa se a __post_init__ da SDKConfig cria um logger padrão
    quando nenhum é fornecido.
    """
    # 1. Preparação: Nenhuma preparação extra necessária.
    # 2. Execução: Criamos a configuração.
    config = SDKConfig()

    # 3. Verificação:
    # Verificamos se o logger não é None e se é de fato um logger do loguru.
    # A verificação do tipo exato pode ser frágil, então focamos no comportamento.
    # O teste mais importante é que ele responde a métodos de log.
    assert config.logger is not None
    assert hasattr(config.logger, "info")
    assert hasattr(config.logger, "debug")


def test_sdk_with_custom_logger_uses_it_correctly():
    """
    Testa se a SDK utiliza um logger customizado quando um é fornecido.
    """
    # 1. Preparação: Criamos um objeto falso (mock) para ser nosso logger.
    mock_logger = MagicMock()

    # 2. Execução: Passamos o mock_logger para a configuração e inicializamos a SDK.
    config = SDKConfig(logger=mock_logger)
    sdk = ZapGlueAPI(config=config)

    # 3. Verificação: Verificamos se o logger na SDK é o mesmo objeto que passamos.
    # O operador `is` verifica se são o mesmo objeto na memória.
    assert sdk.logger is mock_logger
    assert sdk.config.logger is mock_logger


def test_listings_property_lazy_loads_correctly(mocker):
    """
    Testa se a propriedade `listings` inicializa a classe Listings
    apenas no primeiro acesso.
    """
    # 1. Preparação:
    # Substituímos a classe `Listings` real por um mock para isolar o teste.
    # Isso impede que o código real de `Listings` seja executado.
    mock_listings_class = mocker.patch(
        "datalar.scrapers.zap_imoveis.sdk.routes.listings.Listings"
    )
    sdk = ZapGlueAPI()

    # Verificamos o estado inicial: o atributo privado _listings deve ser None.
    assert sdk._listings is None

    # 2. Execução (Primeiro Acesso):
    listings_instance1 = sdk.listings

    # 3. Verificação (Primeiro Acesso):
    # A classe mock `Listings` deve ter sido chamada uma vez para criar a instância.
    mock_listings_class.assert_called_once_with(sdk)
    # O atributo privado agora deve conter a instância criada.
    assert sdk._listings is not None
    assert sdk._listings == listings_instance1  # Deve ser o mesmo objeto

    # 4. Execução (Segundo Acesso):
    listings_instance2 = sdk.listings

    # 5. Verificação (Segundo Acesso):
    # A classe mock `Listings` NÃO deve ser chamada novamente. A contagem de chamadas ainda é 1.
    mock_listings_class.assert_called_once()
    # A instância retornada deve ser a mesma do primeiro acesso.
    assert listings_instance1 is listings_instance2
