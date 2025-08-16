from typing import Literal

from datalar.scrapers.zap_imoveis.sdk.routes.base import Route
from datalar.scrapers.zap_imoveis.sdk.schemas import FullSearchResponseFields


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

        return resp.content.decode("utf-8", errors="ignore")
