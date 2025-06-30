use pyo3::prelude::*;

pub mod item;
pub mod user;

// use item::{Consumable, KeyItem};
use user::User;

#[pymodule]
fn discord_pyo3_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<User>()?;
    m.add_class::<Consumable>()?;
    m.add_class::<KeyItem>()?;

    Ok(())
}
