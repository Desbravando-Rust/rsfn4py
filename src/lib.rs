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