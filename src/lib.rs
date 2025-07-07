use pyo3::prelude::*;

pub mod items;
pub mod user;

// use item::{Consumable, KeyItem};
use items::item::Item;
use user::User;

// use crate::items::item::Item;
// use crate::user::User;

#[pymodule]
fn snekobjs(_py: Python, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<Item>()?;
    module.add_class::<User>()?;
    Ok(())
}
