import re

def validate_cnpj_python(cnpj: str) -> bool:
    """Valida CNPJ (numérico ou alfanumérico) usando a implementação em Python puro."""
    cnpj = re.sub(r'[^a-zA-Z0-9]', '', cnpj).upper()
    if len(cnpj) != 14:
        return False
        
    def get_ascii_val(char):
        return ord(char) - 48
        
    if len(set(cnpj)) == 1:
        return False
        
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(get_ascii_val(cnpj[i]) * weights1[i] for i in range(12))
    mod1 = sum1 % 11
    dv1 = 0 if mod1 < 2 else 11 - mod1
    if get_ascii_val(cnpj[12]) != dv1:
        return False
        
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = sum(get_ascii_val(cnpj[i]) * weights2[i] for i in range(13))
    mod2 = sum2 % 11
    dv2 = 0 if mod2 < 2 else 11 - mod2
    
    return get_ascii_val(cnpj[13]) == dv2