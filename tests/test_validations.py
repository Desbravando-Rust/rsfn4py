import pytest
from rsfn4py import (
    validate_cnpj_rust,
    validate_cnpj_python,
    validate_cpf_rust,
    validate_cpf_python,
)

# Casos de testes comuns:
# - CNPJ numérico válido
# - Novo CNPJ alfanumérico válido
# - CNPJ inválido por Dígito Verificador (DV) errado
# - CNPJ inválido por repetição (ex: 11.111.111/1111-11)
# - String aleatória sem sentido
cnpj_test_cases = [
    ("12.345.678/0001-95", True),           # Numérico válido genérico formatado
    ("12345678000195", True),               # Numérico válido sem formatação
    ("12ABC34501DE35", True),               # Alfanumérico (IN RFB 2.119/2022) simulado válido
    ("12.345.678/0001-00", False),          # DV Incorreto
    ("11111111111111", False),              # Rejeição de repetição de caracteres
    ("12.ABC.678/000X-95", False),          # Dígito final x não numérico no validador
    ("NONSENSE", False)                     # Totalmente inválido e curto
]

cpf_test_cases = [
    ("529.982.247-25", True),               # CPF válido formatado
    ("52998224725", True),                  # CPF válido sem formatação
    ("529.982.247-24", False),              # DV Incorreto
    ("111.111.111-11", False),              # Rejeição de repetição de dígitos
    ("NONSENSE", False),                    # Totalmente inválido e curto
]

@pytest.mark.parametrize("cnpj, expected", cnpj_test_cases)
def test_rust_cnpj_validation(cnpj, expected):
    """Testa a biblioteca compilada no módulo nativo do PyO3."""
    assert validate_cnpj_rust(cnpj) == expected

@pytest.mark.parametrize("cnpj, expected", cnpj_test_cases)
def test_python_cnpj_validation(cnpj, expected):
    """Testa o fallback em Python puro."""
    assert validate_cnpj_python(cnpj) == expected


@pytest.mark.parametrize("cpf, expected", cpf_test_cases)
def test_rust_cpf_validation(cpf, expected):
    """Testa validação de CPF usando implementação Rust."""
    assert validate_cpf_rust(cpf) == expected


@pytest.mark.parametrize("cpf, expected", cpf_test_cases)
def test_python_cpf_validation(cpf, expected):
    """Testa validação de CPF usando fallback Python."""
    assert validate_cpf_python(cpf) == expected