import pytest
from licitation_filter.filters.licitation_prefilter import LicitationPreFilter

@pytest.fixture
def prefilter():
    pf = LicitationPreFilter()
    pf.valid_codes = set([123, 456])
    pf.all_codes = set([123, 456, 789])
    return pf

def test_pass(prefilter):
    
    licitation = {
        "Items": {
            "Listado": [
                {"CodigoProducto": 123, "NombreProducto": "Product A"},
                {"CodigoProducto": 789, "NombreProducto": "Product B"}
            ]
        }
    }
    result, unregistered = prefilter.UNSPC_filter(licitation)
    assert result == "pass"
    assert unregistered == {}

def test_unregistered(prefilter):
    licitation = {
        "Items": {
            "Listado": [
                {"CodigoProducto": 999, "NombreProducto": "Product X"}
            ]
        }
    }
    result, unregistered = prefilter.UNSPC_filter(licitation)
    assert result == "unregistered"
    assert unregistered == {999: "Product X"}

def test_fail(prefilter):
    licitation = {
        "Items": {
            "Listado": [
                {"CodigoProducto": 789, "NombreProducto": "Product B"}
            ]
        }
    }
    result, unregistered = prefilter.UNSPC_filter(licitation)
    assert result == "fail"
    assert unregistered == {}