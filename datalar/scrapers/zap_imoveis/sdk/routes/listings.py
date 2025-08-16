from typing import Literal

from datalar.scrapers.zap_imoveis.sdk.routes.base import Route
from datalar.scrapers.zap_imoveis.sdk.schemas import FullSearchResponseFields, ListingData


class Listings(Route):

    resource_base_url = "listings"

    def search(
        self,
        *,
        include_fields: FullSearchResponseFields,
        business_type: Literal["SALE", "RENT"] = "SALE",
        listing_type: Literal["DEVELOPMENT", "USED"] = "USED",
        page: int = 1,
        size: int = 10,
        _from: int = 0,
        parse_data: bool = True,
    ):
        assert size > 0, "Size must be greater than 0"
        assert size <= 110, "Size must be less than or equal to 110"

        if page < 1:
            raise ValueError("Page must be greater than or equal to 1")

        payload = {
            "size": size,
            "categoryPage": "RESULT",
            "includeFields": include_fields.generate_string(),
            "businessType": business_type,
            "listingType": listing_type,
            "page": page,
            "from": _from,
        }

        resp = self.get(
            params=payload,
        )
        data = resp.json()
        if not parse_data:
            return data
        return self._parse_listing_data(data)
        
    def _parse_listing_data(self, data: dict) -> list[ListingData]:
        try:
            listings = data["search"]["result"]["listings"]

            parsed_data = []
            for listing in listings:
                try:
                    normalized_data = self._normalize_keys(listing['listing'])
                    parsed_data.append(ListingData(**normalized_data))
                except Exception as e:
                    import ipdb; ipdb.set_trace()
                    self.sdk.logger.error(f"Error parsing listing data: {e}")
                    continue
            return parsed_data

        except KeyError as e:
            raise ValueError(f"Api response does not contain expected keys {e}") from e

    def _normalize_keys(self, data: dict) -> dict:
        """
        Normaliza as chaves do dicionário de dados para o formato esperado pelo modelo ListingData.
        """
        normalized_data = {}
        for key, value in data.items():
            # Converte chaves camelCase para snake_case
            for char in key:
                if char.isupper():
                    key = key.replace(char, f"_{char.lower()}")

            if isinstance(value, dict):
                value = self._normalize_keys(value)
            if isinstance(value, list):
                value = [self._normalize_keys(item) if isinstance(item, dict) else item for item in value]
            normalized_data[key] = value
        return normalized_data
if __name__ == "__main__":
    from datalar.scrapers.zap_imoveis.sdk.sdk import ZapGlueAPI, SDKConfig
    sdk = ZapGlueAPI(SDKConfig(RAISE_FOR_STATUS=False))

    result = sdk.listings.search(
        include_fields=FullSearchResponseFields().include_all(),
        business_type="RENTAL",
        listing_type="USED",
        page=1203403400009999999999999,
        size=110,
    )
    print(result)