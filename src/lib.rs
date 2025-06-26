use pyo3::prelude::*;

mod item;
mod user;

#[pymodule]
fn user(_py: Python<'_>, m: &PyModule) -> PyResult<()> {}

#[pymodule]
fn item(_py: Python<'_>, m: &PyModule) -> PyResult<()> {}
