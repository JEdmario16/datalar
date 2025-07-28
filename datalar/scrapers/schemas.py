from pydantic import BaseModel, Field

from enum import Enum

class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    LAND = "land"
    INDUSTRIAL = "industrial"
    OTHER = "other"

class PropertySchema(BaseModel):
    id: str = Field(..., description="Identificador único do imóvel")
    address: str = Field(..., description="Linha de endereço completo do imóvel")
    city: str = Field(..., description="Cidade onde o imóvel está localizado")
    state: str = Field(..., description="Estado onde o imóvel está localizado")
    zip_code: str = Field(..., description="Código postal do imóvel")
    country: str = Field(..., description="País onde o imóvel está localizado")
    for_rent: bool = Field(..., description="Indica se o imóvel está disponível para aluguel")
    for_sale: bool = Field(..., description="Indica se o imóvel está disponível para venda")
    iptu: float = Field(..., description="Valor do IPTU do imóvel")
    sale_price: float | None = Field(None, description="Preço de venda do imóvel, se aplicável")
    rent_price: float | None = Field(None, description="Preço de aluguel do imóvel, se aplicável")
    bedrooms: int = Field(..., description="Número de quartos no imóvel")
    bathrooms: int = Field(..., description="Número de banheiros no imóvel")
    parking_spaces: int = Field(..., description="Número de vagas de estacionamento disponíveis")
    area: float = Field(..., description="Área total do imóvel em metros quadrados")
    property_type: PropertyType = Field(..., description="Tipo de imóvel (residencial, comercial, etc.)")
    year_built: int | None = Field(None, description="Ano de construção do imóvel")
    has_garden: bool = Field(..., description="Indica se o imóvel possui jardim")
    has_pool: bool = Field(..., description="Indica se o imóvel possui piscina")
    is_furnished: bool = Field(..., description="Indica se o imóvel está mobiliado")
    description: str | None = Field(None, description="Descrição adicional do imóvel")
    images: list[str] = Field(..., description="Lista de URLs das imagens do imóvel")
    url: str = Field(..., description="URL da página do imóvel no site de listagem")
    source: str = Field(..., description="Fonte de onde as informações do imóvel foram extraídas")
    scraped_at: str = Field(..., description="Data e hora em que as informações foram extraídas")
    source_id: str = Field(..., description="Identificador único da fonte de dados do imóvel")
    source_url: str = Field(..., description="URL da fonte de dados do imóvel")
    source_name: str = Field(..., description="Nome da fonte de dados do imóvel")
