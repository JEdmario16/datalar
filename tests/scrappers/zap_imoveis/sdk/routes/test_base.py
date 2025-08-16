from datalar.scrapers.zap_imoveis.sdk.routes.base import Route, NotFoundError
from datalar.scrapers.zap_imoveis.sdk.sdk import SDKConfig, ZapGlueAPI
import responses
from unittest.mock import MagicMock, patch

@responses.activate
def test_raise_for_staus_method_shoul_be_called_when_404():
    api = ZapGlueAPI(SDKConfig(RAISE_FOR_STATUS=True))
    
    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)

    responses.add(responses.GET, api.BASE_URL + "test/listings", status=404)
    try:
        route.get("/listings")
    except Exception as e:
        assert isinstance(e, NotFoundError)
        assert str(e) == f"Resource not found: {api.BASE_URL}test/listings"

@responses.activate
def test_raise_for_status_method_should_not_be_called_when_404_and_raise_for_status_false():
    api = ZapGlueAPI(SDKConfig(RAISE_FOR_STATUS=False))

    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)

    responses.add(responses.GET, api.BASE_URL + "test/listings", status=404)

    with patch.object(route, 'raise_for_status', wraps=route.raise_for_status) as mock_method:
        response = route.get("/listings")
        assert response.status_code == 404
        mock_method.assert_not_called()

@responses.activate
def test_raise_for_status_method_should_be_called_when_500():
    api = ZapGlueAPI(SDKConfig(RAISE_FOR_STATUS=True))

    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)

    responses.add(responses.GET, api.BASE_URL + "test/listings", status=500)
    try:
        route.get("/listings")
    except Exception as e:
        assert isinstance(e, NotFoundError) is False
        assert "HTTP error 500" in str(e)


@responses.activate
def test_route_build_url_when_resource_name_is_provided():
    api = ZapGlueAPI()
    
    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)
    full_url = route.build_url(resource_name="listings")
    assert full_url == api.BASE_URL + "test/listings"

@responses.activate
def test_route_build_url_when_resource_name_is_not_provided():
    api = ZapGlueAPI()

    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)
    full_url = route.build_url()
    assert full_url == api.BASE_URL + "test"

@responses.activate
def test_route_build_url_when_resource_name_is_empty_string():
    api = ZapGlueAPI()

    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)
    full_url = route.build_url(resource_name="")
    assert full_url == api.BASE_URL + "test"

@responses.activate
def test_route_build_url_when_resource_name_starts_with_slash():
    api = ZapGlueAPI()
    
    class TestRoute(Route):
        resource_base_url = "test" 
    
    route = TestRoute(api)
    full_url = route.build_url(resource_name="/listings")
    assert full_url == api.BASE_URL + "test/listings"

@responses.activate
def test_route_when_log_error_is_true():
    api = ZapGlueAPI(SDKConfig(LOG_LEVEL="DEBUG", LOG_REQUESTS=True, LOG_RESPONSES=True))
    
    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)

    resp = responses.add(responses.GET, api.BASE_URL + "test/listings", status=404)
    with patch.object(api.logger, 'error') as mock_log_error:
        try:
            route.get("/listings")
        except NotFoundError:
            pass
        mock_log_error.assert_called_once_with(f"Error in {route.__class__.__name__}: Resource not found: {api.BASE_URL}test/listings")

@responses.activate
def test_route_when_log_response_is_true():
    api = ZapGlueAPI(SDKConfig(LOG_LEVEL="DEBUG", LOG_REQUESTS=False, LOG_RESPONSES=True))
    
    class TestRoute(Route):
        resource_base_url = "test"

    route = TestRoute(api)
    resp = responses.Response(method=responses.GET, url=api.BASE_URL + "test/listings", json={"data": "test"}, status=200)
    responses.add(resp)
    with patch.object(api.logger, 'debug') as mock_log_response:
        response = route.get("/listings")
        mock_log_response.assert_called_once_with(f"Response from {resp.url} (status: {response.status_code}): {response.content.decode('utf-8', errors='ignore')}")