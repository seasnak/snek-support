use pyo3::prelude::*;
use std::collections::HashMap;

use crate::items::item;

#[pyclass]
#[derive(Copy, Clone, Debug, PartialEq)]
pub struct User {
    #[pyo3(get, set)]
    pub id: i64,
    #[pyo3(get, set)]
    pub username: String,
    #[pyo3(get, set)]
    pub social_credit: i16,
    #[pyo3(get, set)]
    pub coins: u16,
    pub items: HashMap<String, u16>,
}

#[pymethods]
impl User {
    #[new]
    fn new(id: i64, name: String, social_credit: i16, coins: Option<u16>) -> Self {
        let num_coins: u16 = match coins {
            Some(p) => p,
            None => 0,
        };

        User {
            id: id,
            username: name,
            social_credit: social_credit,
            coins: num_coins,
            items: HashMap::new(),
        }
    }

    pub fn add_item(&mut self, name: String, item: &item::Item) {
        if self.items.contains_key(&name) {}
        self.items.insert(name, *item);
    }
}
