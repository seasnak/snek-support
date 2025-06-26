use pyo3::prelude::*;

#[pyclass]
struct Item {
    #[pyo3(get)]
    pub name: String,
    pub quantity: i8,
}

#[pymethods]
impl Item {
    #[new]
    fn new(item_name: String, item_quantity: Option<i8>) -> Self {
        let num_items = match item_quantity {
            Some(n) => n,
            None => 1,
        };

        Item {
            name: item_name, // might need to do a copy?
            quantity: num_items,
        }
    }
}

impl Copy for Item {
    fn copy(&self) -> Self {
        Item {
            name: self.name.clone(),
            quantity: self.quantity,
        }
    }
}
