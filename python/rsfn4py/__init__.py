from .rsfn4py import validate_cnpj_rust, validate_cpf_rust
from .validations import validate_cnpj_python, validate_cpf_python

__all__ = [
	"validate_cnpj_rust",
	"validate_cnpj_python",
	"validate_cpf_rust",
	"validate_cpf_python",
]