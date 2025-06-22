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
    #[pyo3(get, set)]
    pub name: String,
    #[pyo3(get, set)]
    pub social_credit: i16,
    pub items: HashMap<String, Item>,
}

#[pymethods]
impl User {
    #[new]
    fn new(id: i64, name: String, social_credit: i16) -> Self {
        User {
            id,
            name,
            social_credit,
            items: HashMap::new(),
        }
    }

    pub fn add_item(&mut self, name: String, item: &Item) {
        if self.items.contains_key(&name) {}
        self.items.insert(name, *item);
    }
}
