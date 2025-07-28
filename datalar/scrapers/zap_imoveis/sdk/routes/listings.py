from datalar.scrapers.zap_imoveis.sdk.routes.base import Route

from typing import Literal

class Listings(Route):

    resource_base_url = "listings"

    def search(
        self,
        *,
        portal: Literal["zap"] = "zap",
        category_page: Literal["RESULT"] = "RESULT",
        business_type: Literal["SALE", "RENT"] = "SALE",
        parent_id: str | None = None,
        listing_type: Literal["DEVELOPMENT", "USED"] = "USED",
    ):
        ...
