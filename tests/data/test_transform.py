import pytest

from datetime import datetime
from src.data.transform import Transformer


CURRENT_EXECUTION_DATE = datetime.now()


DOCUMENT_TEMPLATE = {
    "OBJECTID": 16,
    "Country_Region": "Switzerland",
    "Last_Update": 1585506823000,
    "Lat": 46.8182,
    "Long_": 8.2275,
    "Confirmed": 14829,
    "Deaths": 300,
    "Recovered": 1595,
    "Active": 12934,
}

RESPONSE_TEMPLATE = {
    "updated": CURRENT_EXECUTION_DATE,
    "confirmed": 14829,
    "deaths": 300,
    "recovered": 1595,
    "location": {"lon": 8.2275, "lat": 46.8182},
    "country_name": "Switzerland",
}


class TestTransformer:
    @pytest.fixture()
    def transformer(self):
        return Transformer()

    def test_generate_document_output(self, transformer):
        generated_doc = transformer.generate_document(
            DOCUMENT_TEMPLATE, CURRENT_EXECUTION_DATE
        )

        assert generated_doc == RESPONSE_TEMPLATE

    def test_generate_document_output_type(self, transformer):
        generated_doc = transformer.generate_document(
            DOCUMENT_TEMPLATE, CURRENT_EXECUTION_DATE
        )

        assert type(generated_doc) == dict

    def test_generate_document_errors(self, transformer):
        with pytest.raises(TypeError):
            transformer.generate_document("", CURRENT_EXECUTION_DATE)
