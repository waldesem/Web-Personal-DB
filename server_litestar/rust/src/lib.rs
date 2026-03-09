use pyo3::prelude::*;

/// Validate snils
#[pyfunction]
fn validate_snils(snils: Option<&str>) -> PyResult<Option<String>> {
    let snils = match snils {
        Some(s) => s,
        None => return Ok(None),
    };

    let cleaned: String = snils.chars().filter(|c| c.is_ascii_digit()).collect();

    if cleaned.len() != 11 {
        return Ok(None);
    }

    let digits: Vec<u32> = cleaned.chars().map(|c| c.to_digit(10).unwrap()).collect();

    let main_part = &digits[..9];
    let check_sum = digits[9] * 10 + digits[10];

    let sum_prod: u32 = main_part
        .iter()
        .enumerate()
        .map(|(i, &d)| d * (9 - i as u32))
        .sum();

    let calculated_sum = if sum_prod < 100 {
        sum_prod
    } else if sum_prod == 100 || sum_prod == 101 {
        0
    } else {
        let remainder = sum_prod % 101;
        if remainder == 100 {
            0
        } else {
            remainder
        }
    };

    if calculated_sum == check_sum {
        Ok(Some(cleaned))
    } else {
        Ok(None)
    }
}

/// Validate inn
#[pyfunction]
fn validate_inn(inn: Option<&str>) -> PyResult<Option<String>> {
    let inn = match inn {
        Some(s) => s,
        None => return Ok(None),
    };

    let cleaned: String = inn.chars().filter(|c| c.is_ascii_digit()).collect();

    if cleaned.len() != 12 {
        return Ok(None);
    }

    let digits: Vec<u32> = cleaned.chars().map(|c| c.to_digit(10).unwrap()).collect();

    let c1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0];
    let c2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0];

    let check1 = digits
        .iter()
        .zip(c1.iter())
        .map(|(&d, &c)| d * c)
        .sum::<u32>()
        % 11
        % 10;
    let check2 = digits
        .iter()
        .zip(c2.iter())
        .map(|(&d, &c)| d * c)
        .sum::<u32>()
        % 11
        % 10;

    if check1 == digits[10] && check2 == digits[11] {
        Ok(Some(cleaned))
    } else {
        Ok(None)
    }
}

#[pymodule]
fn checksum(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_snils, m)?)?;
    m.add_function(wrap_pyfunction!(validate_inn, m)?)?;
    Ok(())
}
