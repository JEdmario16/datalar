from pydantic import BaseModel, Field

from typing import Literal

class BaseFieldsModel(BaseModel):
    """
    Base model for fields that can be included in search responses.
    This model can be extended to create specific field models for different objects.
    """

    def only(self, *fields):
        """
        Retorna uma nova instância do modelo contendo apenas os campos especificados.
        """
        data = {f: (f in fields) for f in self.model_fields.keys()}
        return self.__class__(**data)

    def include_all(self):
        """
        Retorna uma nova instância do modelo contendo todos os campos.
        """
        data = {}
        for f, v in self.__class__.model_fields.items():
            if isinstance(v.default, bool):
                data[f] = True
            else:
                data[f] = v.default_factory().include_all()
        return self.__class__(**data)

    def generate_string(self, is_subfield: bool=False) -> str:
        """
        Gera uma string representando os campos incluídos na busca.
        Essa é a string utilizada como parâmetor na requisição de busca.
        Ela possui o seguinte formato:
        objeto(
            campo1,
            campo2,
            subobjeto(
                subcampo1,
                subcampo2,
            ),
        )
        """
        data_str = "(" if is_subfield else ""
        for k, v in self.__class__.model_fields.items():
            if isinstance(v.default, bool):
                if self.__getattribute__(k):
                    # transforma a chave de snake_case para camelCase
                    k = k.replace("_", " ").title().replace(" ", "")
                    k = k[0].lower() + k[1:]  # primeira letra minúscula
                    data_str += f"{k}, "
            else:
                sub_fields = self.__getattribute__(k)
                if isinstance(sub_fields, BaseFieldsModel):
                    subfield = f"{k}{sub_fields.generate_string(is_subfield=True)}, "
                    if subfield == f"{k}(), ":
                        continue
                    data_str += subfield
        data_str = data_str.rstrip(", ")
        data_str += ")" if is_subfield else ""
        return data_str

class ListingSearchFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados referentes ao objeto Listing na busca de listagens da API.
    O objeto Listing contém informações detalhadas sobre imóveis disponíveis para venda ou aluguel.
    """

    contract_type: bool = Field(
        default=False,
        description="Indica se o tipo de contrato deve ser incluído nos resultados.",
    )
    listings_count: bool = Field(
        default=False,
        description="Indica se a contagem de listagens deve ser incluída nos resultados.",
    )
    property_developers: bool = Field(
        default=False,
        description="Indica se os desenvolvedores de propriedades devem ser incluídos nos resultados.",
    )
    source_id: bool = Field(
        default=False,
        description="Indica se o ID da fonte deve ser incluído nos resultados.",
    )
    display_address_type: bool = Field(
        default=False,
        description="Indica se o tipo de endereço exibido deve ser incluído nos resultados.",
    )
    amenities: bool = Field(
        default=False,
        description="Indica se as comodidades devem ser incluídas nos resultados.",
    )
    usable_areas: bool = Field(
        default=False,
        description="Indica se as áreas utilizáveis devem ser incluídas nos resultados.",
    )
    construction_status: bool = Field(
        default=False,
        description="Indica se o status de construção deve ser incluído nos resultados.",
    )
    listing_type: bool = Field(
        default=False,
        description="Indica se o tipo de listagem deve ser incluído nos resultados.",
    )
    description: bool = Field(
        default=False,
        description="Indica se a descrição da listagem deve ser incluída nos resultados.",
    )
    title: bool = Field(
        default=False,
        description="Indica se o título da listagem deve ser incluído nos resultados.",
    )
    stamps: bool = Field(
        default=False,
        description="Indica se os selos devem ser incluídos nos resultados.",
    )
    created_at: bool = Field(
        default=False,
        description="Indica se a data de criação deve ser incluída nos resultados.",
    )
    floors: bool = Field(
        default=False,
        description="Indica se os andares devem ser incluídos nos resultados.",
    )
    unit_types: bool = Field(
        default=False,
        description="Indica se os tipos de unidade devem ser incluídos nos resultados.",
    )
    non_activation_reason: bool = Field(
        default=False,
        description="Indica se o motivo de não ativação deve ser incluído nos resultados.",
    )
    provider_id: bool = Field(
        default=False,
        description="Indica se o ID do provedor deve ser incluído nos resultados.",
    )
    property_type: bool = Field(
        default=False,
        description="Indica se o tipo de propriedade deve ser incluído nos resultados.",
    )
    unit_sub_types: bool = Field(
        default=False,
        description="Indica se os subtipos de unidade devem ser incluídos nos resultados.",
    )
    units_on_the_floor: bool = Field(
        default=False,
        description="Indica se as unidades no andar devem ser incluídas nos resultados.",
    )
    legacy_id: bool = Field(
        default=False,
        description="Indica se o ID legado deve ser incluído nos resultados.",
    )
    id: bool = Field(
        default=False,
        description="Indica se o ID da listagem deve ser incluído nos resultados.",
    )
    portal: bool = Field(
        default=False,
        description="Indica se o portal deve ser incluído nos resultados.",
    )
    unit_floor: bool = Field(
        default=False,
        description="Indica se o andar da unidade deve ser incluído nos resultados.",
    )
    parking_spaces: bool = Field(
        default=False,
        description="Indica se as vagas de estacionamento devem ser incluídas nos resultados.",
    )
    updated_at: bool = Field(
        default=False,
        description="Indica se a data de atualização deve ser incluída nos resultados.",
    )
    address: bool = Field(
        default=False,
        description="Indica se o endereço deve ser incluído nos resultados.",
    )
    suites: bool = Field(
        default=False,
        description="Indica se as suítes devem ser incluídas nos resultados.",
    )
    publication_type: bool = Field(
        default=False,
        description="Indica se o tipo de publicação deve ser incluído nos resultados.",
    )
    external_id: bool = Field(
        default=False,
        description="Indica se o ID externo deve ser incluído nos resultados.",
    )
    bathrooms: bool = Field(
        default=False,
        description="Indica se os banheiros devem ser incluídos nos resultados.",
    )
    usage_types: bool = Field(
        default=False,
        description="Indica se os tipos de uso devem ser incluídos nos resultados.",
    )
    total_areas: bool = Field(
        default=False,
        description="Indica se as áreas totais devem ser incluídas nos resultados.",
    )
    advertiser_id: bool = Field(
        default=False,
        description="Indica se o ID do anunciante deve ser incluído nos resultados.",
    )
    advertiser_contact: bool = Field(
        default=False,
        description="Indica se o contato do anunciante deve ser incluído nos resultados.",
    )
    whatsapp_number: bool = Field(
        default=False,
        description="Indica se o número do WhatsApp deve ser incluído nos resultados.",
    )
    bedrooms: bool = Field(
        default=False,
        description="Indica se os quartos devem ser incluídos nos resultados.",
    )
    accept_exchange: bool = Field(
        default=False,
        description="Indica se a troca é aceita na listagem.",
    )
    pricing_infos: bool = Field(
        default=False,
        description="Indica se as informações de preços devem ser incluídas nos resultados.",
    )
    show_price: bool = Field(
        default=False,
        description="Indica se o preço deve ser exibido na listagem.",
    )
    resale: bool = Field(
        default=False,
        description="Indica se a venda é uma revenda.",
    )
    buildings: bool = Field(
        default=False,
        description="Indica se os edifícios devem ser incluídos nos resultados.",
    )
    capacity_limit: bool = Field(
        default=False,
        description="Indica se o limite de capacidade deve ser incluído nos resultados.",
    )
    status: bool = Field(
        default=False,
        description="Indica se o status da listagem deve ser incluído nos resultados.",
    )
    price_suggestion: bool = Field(
        default=False,
        description="Indica se a sugestão de preço deve ser incluída nos resultados.",
    )
    condominium_name: bool = Field(
        default=False,
        description="Indica se o nome do condomínio deve ser incluído nos resultados.",
    )
    modality: bool = Field(
        default=False,
        description="Indica se a modalidade da listagem deve ser incluída nos resultados.",
    )
    enhanced_development: bool = Field(
        default=False,
        description="Indica se o desenvolvimento aprimorado deve ser incluído nos resultados.",
    )


class AccountSearchFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados referentes ao objeto Account na busca de listagens da API.
    Account aqui representa o anunciante ou proprietário do imóvel.
    """

    id: bool = Field(
        default=False,
        description="Indica se o ID da conta deve ser incluído nos resultados.",
    )
    name: bool = Field(
        default=False,
        description="Indica se o nome da conta deve ser incluído nos resultados.",
    )
    logo_url: bool = Field(
        default=False,
        description="Indica se a URL do logotipo da conta deve ser incluída nos resultados.",
    )
    license_number: bool = Field(
        default=False,
        description="Indica se o número de licença da conta deve ser incluído nos resultados.",
    )
    show_address: bool = Field(
        default=False,
        description="Indica se o endereço da conta deve ser exibido nos resultados.",
    )
    legacy_vivareal_id: bool = Field(
        default=False,
        description="Indica se o ID legado do VivaReal deve ser incluído nos resultados.",
    )
    legacy_zap_id: bool = Field(
        default=False,
        description="Indica se o ID legado do Zap deve ser incluído nos resultados.",
    )
    created_date: bool = Field(
        default=False,
        description="Indica se a data de criação da conta deve ser incluída nos resultados.",
    )
    tier: bool = Field(
        default=False,
        description="Indica se o nível da conta deve ser incluído nos resultados.",
    )
    trust_score: bool = Field(
        default=False,
        description="Indica se a pontuação de confiança da conta deve ser incluída nos resultados.",
    )
    total_count_by_filter: bool = Field(
        default=False,
        description="Indica se a contagem total por filtro deve ser incluída nos resultados.",
    )
    total_count_by_advertiser: bool = Field(
        default=False,
        description="Indica se a contagem total por anunciante deve ser incluída nos resultados.",
    )


class ListingChildrenSearchFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados referentes ao objeto `Children` na busca de listagens da API.
    O objeto `Children` contém atributos relacionados ao imóvel, como áreas, quartos, banheiros, etc.
    """

    id: bool = Field(
        default=False,
        description="Indica se o ID do filho deve ser incluído nos resultados.",
    )
    usable_areas: bool = Field(
        default=False,
        description="Indica se as áreas utilizáveis do filho devem ser incluídas nos resultados.",
    )
    total_areas: bool = Field(
        default=False,
        description="Indica se as áreas totais do filho devem ser incluídas nos resultados.",
    )
    bedrooms: bool = Field(
        default=False,
        description="Indica se o número de quartos do filho deve ser incluído nos resultados.",
    )
    bathrooms: bool = Field(
        default=False,
        description="Indica se o número de banheiros do filho deve ser incluído nos resultados.",
    )
    parking_spaces: bool = Field(
        default=False,
        description="Indica se o número de vagas de estacionamento do filho deve ser incluído nos resultados.",
    )
    pricing_infos: bool = Field(
        default=False,
        description="Indica se as informações de preços do filho devem ser incluídas nos resultados.",
    )


class ListingsSearchResponseFields(BaseFieldsModel):
    """
    Indica os campos que podem ser recuperados referentes ao objeto `Listings` na busca de listagens da API.
    Não confundir com o objeto `Listing`, representado por `ListingSearchFields`.
    Trata-se de um 'container' de objetos e possui dados sobre a listagem, como detalhes do imóvel, anunciante, mídias, etc.
    Veja seus subobjetos para detalhes adicionais.
    """

    listing: ListingSearchFields = Field(
        default_factory=ListingSearchFields,
        description="Campos relacionados à listagem do imóvel.",
    )
    account: AccountSearchFields = Field(
        default_factory=AccountSearchFields,
        description="Campos relacionados à conta do anunciante ou proprietário do imóvel.",
    )
    medias: bool = Field(
        default=False,
        description="Indica se as mídias (fotos, vídeos) devem ser incluídas nos resultados.",
    )
    account_link: bool = Field(
        default=False,
        description="Indica se o link para a conta do anunciante deve ser incluído nos resultados.",
    )
    link: bool = Field(
        default=False,
        description="Indica se o link para a listagem deve ser incluído nos resultados.",
    )
    children: ListingChildrenSearchFields = Field(
        default_factory=ListingChildrenSearchFields,
        description="Campos relacionados aos filhos da listagem, como áreas e quartos.",
    )


class ResultSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de listagens da API.
    Contém informações sobre as listagens encontradas e o total de resultados.
    """

    listings: ListingsSearchResponseFields = Field(
        default_factory=ListingsSearchResponseFields,
        description="Campos relacionados às listagens encontradas na busca.",
    )


class SearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de listagens da API.
    Contém o resultado da busca e o total de resultados encontrados.
    """

    result: ResultSearchResponseFields = Field(
        default_factory=ResultSearchResponseFields,
        description="Campos relacionados ao resultado da busca de listagens.",
    )
    total_count: bool = Field(
        default=False,
        description="Indica se a contagem total de resultados deve ser incluída na resposta.",
    )


class DevelopmentsSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de desenvolvimentos da API.
    Contém informações sobre os desenvolvimentos encontrados e o total de resultados.
    """

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de desenvolvimentos.",
    )


class ExpansionSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de expansões da API.
    Contém informações sobre as expansões encontradas e o total de resultados.
    """

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de expansões.",
    )


class NearbySearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de proximidades da API.
    Contém informações sobre as listagens próximas e o total de resultados.
    """

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de listagens próximas.",
    )


class SuperPremiumSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de listagens super premium da API.
    Contém informações sobre as listagens super premium encontradas e o total de resultados.
    """

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de listagens super premium.",
    )


class TopoFixoSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de listagens topo fixo da API.
    Contém informações sobre as listagens topo fixo encontradas e o total de resultados.
    """

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de listagens topo fixo.",
    )


class FullSearchResponseFields(BaseFieldsModel):
    """
    Representa os campos que podem ser recuperados na resposta de busca de listagens da API.
    Contém informações sobre as listagens encontradas e o total de resultados.
    Consulte os subobjetos para detalhes adicionais.
    """

    developments: DevelopmentsSearchResponseFields = Field(
        default_factory=DevelopmentsSearchResponseFields,
        description="Campos relacionados à busca de desenvolvimentos.",
    )
    expansion: ExpansionSearchResponseFields = Field(
        default_factory=ExpansionSearchResponseFields,
        description="Campos relacionados à busca de expansões.",
    )
    nearby: NearbySearchResponseFields = Field(
        default_factory=NearbySearchResponseFields,
        description="Campos relacionados à busca de listagens próximas.",
    )

    search: SearchResponseFields = Field(
        default_factory=SearchResponseFields,
        description="Campos relacionados à busca de listagens.",
    )

    super_premium: SuperPremiumSearchResponseFields = Field(
        default_factory=SuperPremiumSearchResponseFields,
        description="Campos relacionados à busca de listagens super premium.",
    )
    topo_fixo: TopoFixoSearchResponseFields = Field(
        default_factory=TopoFixoSearchResponseFields,
        description="Campos relacionados à busca de listagens topo fixo.",
    )
    page: bool = Field(
        default=False,
        description="Indica se a paginação deve ser incluída na resposta.",
    )
    full_uri_fragments: bool = Field(
        default=False,
        description="Indica se os fragmentos de URI completos devem ser incluídos na resposta.",
    )



if __name__ == "__main__":
    # Exemplo de uso
    fields = FullSearchResponseFields()
    import ipdb; ipdb.set_trace()