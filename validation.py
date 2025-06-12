import re
from validate_docbr import CPF, CNPJ


def validar_cpf(valor: str) -> bool:
    """Valida CPF removendo caracteres nao numericos."""
    return CPF().validate(re.sub(r"\D", "", valor))


def validar_cnpj(valor: str) -> bool:
    """Valida CNPJ removendo caracteres nao numericos."""
    return CNPJ().validate(re.sub(r"\D", "", valor))
