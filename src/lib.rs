use pyo3::prelude::*;

#[pyfunction]
fn validate_cnpj_rust(cnpj: &str) -> bool {
    let cleaned: Vec<char> = cnpj.chars()
        .filter(|c| c.is_ascii_alphanumeric())
        .map(|c| c.to_ascii_uppercase())
        .collect();
        
    if cleaned.len() != 14 {
        return false;
    }
    
    // Rejeita caso todos os caracteres sejam iguais
    if cleaned.iter().all(|&c| c == cleaned[0]) {
        return false;
    }
    
    let get_val = |c: char| -> i32 { c as i32 - 48 };
    
    // Cálculo do primeiro dígito (DV1)
    let weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let mut sum1 = 0;
    for i in 0..12 {
        sum1 += get_val(cleaned[i]) * weights1[i];
    }
    let mod1 = sum1 % 11;
    let dv1 = if mod1 < 2 { 0 } else { 11 - mod1 };
    
    if get_val(cleaned[12]) != dv1 {
        return false;
    }
    
    // Cálculo do segundo dígito (DV2)
    let weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let mut sum2 = 0;
    for i in 0..13 {
        sum2 += get_val(cleaned[i]) * weights2[i];
    }
    let mod2 = sum2 % 11;
    let dv2 = if mod2 < 2 { 0 } else { 11 - mod2 };
    
    get_val(cleaned[13]) == dv2
}

#[pymodule]
fn rsfn4py(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_cnpj_rust, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::validate_cnpj_rust;

    #[test]
    fn should_accept_valid_numeric_cnpj_with_formatting() {
        assert!(validate_cnpj_rust("12.345.678/0001-95"));
    }

    #[test]
    fn should_accept_valid_numeric_cnpj_without_formatting() {
        assert!(validate_cnpj_rust("12345678000195"));
    }

    #[test]
    fn should_accept_valid_alphanumeric_cnpj() {
        assert!(validate_cnpj_rust("12ABC34501DE35"));
    }

    #[test]
    fn should_accept_lowercase_alphanumeric_cnpj() {
        assert!(validate_cnpj_rust("12abc34501de35"));
    }

    #[test]
    fn should_accept_valid_cnpj_with_extra_non_alphanumeric_chars() {
        assert!(validate_cnpj_rust("..12.345.678/0001-95--"));
    }

    #[test]
    fn should_reject_cnpj_with_invalid_check_digits() {
        assert!(!validate_cnpj_rust("12.345.678/0001-00"));
    }

    #[test]
    fn should_reject_repeated_characters() {
        assert!(!validate_cnpj_rust("11111111111111"));
    }

    #[test]
    fn should_reject_repeated_alphabetic_characters() {
        assert!(!validate_cnpj_rust("AAAAAAAAAAAAAA"));
    }

    #[test]
    fn should_reject_invalid_characters_in_check_digit() {
        assert!(!validate_cnpj_rust("12.ABC.678/000X-95"));
    }

    #[test]
    fn should_reject_nonsense_input() {
        assert!(!validate_cnpj_rust("NONSENSE"));
    }

    #[test]
    fn should_reject_when_cleaned_length_is_not_14() {
        assert!(!validate_cnpj_rust("12.345.678/0001-9500"));
    }

    #[test]
    fn should_reject_empty_input() {
        assert!(!validate_cnpj_rust(""));
    }
}