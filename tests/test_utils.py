import pytest
from src.utils import eleva_quadrado

@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected
    

def test_eleva_quadrado_falha():
    with pytest.raises(TypeError) as exc:
        eleva_quadrado("a")
        
        assert str(exc.value) == "unsupported operand type(s) for ** or pow(): 'str' and 'int'"
        

