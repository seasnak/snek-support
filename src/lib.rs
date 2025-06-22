use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use std::collections::HashMap;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn snek_support(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}

#[pyclass]
struct Item {
    #[pyo3(get)]
    pub name: String,
    pub quantity: i8,
}

#[pyclass]
struct User {
    #[pyo3(get, set)]
    pub id: i64,
    pub name: String,
    pub social_credit: i16,

    #[pyo3(get)]
    pub items: HashMap<String, Item>,
}

#[pymethods]
impl User {
    #[new]
    fn new(id: i64, name: String, social_credit: Option<i16>) -> Self {
        User {
            id,
            name,
            social_credit.unwrap_or(1000),
            {},
        }
    }
}

