from datalar.scrapers.zap_imoveis.sdk.routes.base import Route
from datalar.scrapers.zap_imoveis.sdk.schemas import FullSearchResponseFields

from typing import Literal, Optional

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
    ):
        assert page > 0, "Page number must be greater than 0"
        assert page < 110, "Page number must be less than 110"


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

        return resp.text    


if __name__ == "__main__":
    from datalar.scrapers.zap_imoveis.sdk.sdk import ZapGlueAPI, SDKConfig

    sdk = ZapGlueAPI(config=SDKConfig())
    listings = sdk.listings

    response = listings.search(
        include_fields=FullSearchResponseFields().include_all(),
        business_type="SALE",
        listing_type="USED",
        page=1,
        size=10,
    )

    print(response)