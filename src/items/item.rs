use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug)]
pub struct Item {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub description: String,

    #[pyo3(get)]
    pub quantity: u8,
}

pub trait Price {
    const PRICE: u8;
}

impl Price for Item {
    const PRICE: u8 = 100;
}

pub trait Reusable {
    const IS_REUSABLE: bool;
}

impl Reusable for Item {
    const IS_REUSABLE: bool = false;
}

pub trait Usable {
    fn use_item(&mut self) -> Result<String, String>;
}

impl Usable for Item {
    fn use_item(&mut self) -> Result<String, String> {
        if self.quantity == 0 {
            return Err(format!("No more {}!", self.name));
        }
        self.quantity -= 1;

        Ok(format!(""))
    }
}

#[pymethods]
impl Item {
    #[new]
    pub fn new(item_name: String, quantity: Option<u8>) -> Self {
        let num_items: u8 = match quantity {
            Some(n) => n,
            None => 1,
        };

        Item {
            name: item_name,
            description: String::new(),
            quantity: num_items,
        }
    }

    #[getter]
    pub fn get_description(&mut self) -> PyResult<&String> {
        Ok(&self.description)
    }

    #[setter]
    pub fn set_description(&mut self, value: String) -> PyResult<()> {
        self.description = value;
        Ok(())
    }
}
