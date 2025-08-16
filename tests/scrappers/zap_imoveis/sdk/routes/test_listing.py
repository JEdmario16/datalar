from unittest.mock import MagicMock, patch

import pytest
import responses

from datalar.scrapers.zap_imoveis.sdk.routes.listings import Listings
from datalar.scrapers.zap_imoveis.sdk.sdk import SDKConfig, ZapGlueAPI


@responses.activate
def test_listing_search_route_should_return_valid_response():
    resp = responses.Response(
        method=responses.GET,
        url="https://glue-api.zapimoveis.com.br/v2/listings?size=10&categoryPage=RESULT&businessType=SALE&listingType=USED&page=1&from=0",
        json={"data": "mocked response"},
        status=200,
    )
    responses.add(resp)

    sdk = ZapGlueAPI(config=SDKConfig(RAISE_FOR_STATUS=False))
    resp = sdk.listings.search(
        include_fields=MagicMock(),
        business_type="SALE",
        listing_type="USED",
        page=1,
        size=10,
    )

    assert resp == '{"data": "mocked response"}', "Response should match mocked data"






@pytest.mark.parametrize(
    "page, expected_error",
    [
        (0, "Page number must be greater than 0"),
        (111, "Page number must be less than 110"),
    ],
)
def test_listing_search_route_should_raise_error_if_page_is_out_of_bounds(
    page, expected_error
):
    """
    Testa se a função `search` da rota `Listings` levanta um erro
    quando o número da página está fora dos limites permitidos.
    """
    sdk = ZapGlueAPI(config=SDKConfig(RAISE_FOR_STATUS=False))

    with patch("datalar.scrapers.zap_imoveis.sdk.routes.base.Route.get") as mock_get:
        with pytest.raises(AssertionError, match=expected_error):
            sdk.listings.search(
                include_fields=MagicMock(),
                business_type="SALE",
                listing_type="USED",
                page=page,
                size=10,
            )
        assert (
            not mock_get.called
        ), "GET request should not be called with invalid page number"
