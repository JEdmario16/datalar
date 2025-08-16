from datalar.scrapers.zap_imoveis.sdk import schemas
import pytest
import re

def test_search_fields_selection_with_no_fields():
    fields = schemas.ListingSearchFields(

    )
    assert fields.generate_string() == ""

def test_search_fields_selection_with_some_fields():
    fields = schemas.ListingSearchFields(
        id=True,
        title=True,
        source_id=True,
    )
    generated_str = fields.generate_string()
    assert "id" in generated_str
    assert "title" in generated_str
    assert "sourceId" in generated_str
    assert re.match(r"^[a-zA-Z]+(,\s{1}[a-zA-Z]+)*$", generated_str) is not None
    assert len(generated_str.split(',')) == 3

def test_search_fields_selection_with_nested_objects():
    listing_fields = schemas.ListingSearchFields(
        id=True,
        title=True,
        source_id=True,
    )
    listings_fields = schemas.ListingsSearchResponseFields(
        listing=listing_fields
    )
    generated_str = listings_fields.generate_string()
    assert "listing(" in generated_str
    assert generated_str.endswith(")")
    assert "id" in generated_str
    assert "title" in generated_str
    assert "sourceId" in generated_str
    assert re.match(r"^listing\([a-zA-Z]+(,\s{1}[a-zA-Z]+)*\)$", generated_str) is not None
    assert len(generated_str[generated_str.index('(')+1:-1].split(',')) == 3

@pytest.mark.parametrize("field", [
    "search",
    "result",
        "listings",
        "listing",
        "address",
        "developments",
        "expansion",
        "nearby",
        "super_premium",
        "topo_fixo"
    ]
)
def test_search_fields_selection_with_all_fields(field):
    fields = schemas.FullSearchResponseFields().include_all()
    generated_str = fields.generate_string()
    assert field in generated_str


def test_search_fields_selection_with_no_fields_in_nested_object():
    listing = schemas.ListingSearchFields()
    listings_fields = schemas.ListingsSearchResponseFields(
        listing=listing
    )
    generated_str = listings_fields.generate_string()
    assert generated_str == ""

def test_full_search_response_fields_with_only_one_feature():
    fields = schemas.FullSearchResponseFields(
        search=schemas.SearchResponseFields(
            total_count=True
        )
    )
    generated_str = fields.generate_string()
    assert generated_str == "search(totalCount)"

def test_full_search_response_fields_with_multiple_features():
    fields = schemas.FullSearchResponseFields(
        search=schemas.SearchResponseFields(
            total_count=True,
        ),
        expansion=schemas.ExpansionSearchResponseFields(
            search=schemas.SearchResponseFields(
                total_count=True
            ),
        )
        
    )
    generated_str = fields.generate_string()
    assert "search(totalCount)" in generated_str
    assert "expansion(search(totalCount))" in generated_str
    assert len(generated_str.split(',')) == 2