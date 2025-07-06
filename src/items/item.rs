use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Debug)]
pub struct Item {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get, set)]
    pub price: u8,
    pub max_quantity: u8,
    pub is_keyitem: bool,
}

#[pymethods]
impl Item {
    #[new]
    fn new(item_name: String, max_item_quantity: Option<u8>, price: Option<u8>) -> Self {
        let max_num_items: u8 = match max_item_quantity {
            Some(n) => n,
            None => 99,
        };

        let item_price: u8 = match price {
            Some(n) => n,
            None => 100,
        };

        Item {
            name: item_name,
            description: String::new(),
            price: price,
            max_quantity: max_num_items,
            is_keyitem: false,
        }
    }

    #[getter]
    fn get_max_quantity(&mut self) -> PyResult<u8> {
        Ok(self.max_quantity)
    }

    #[setter]
    fn set_max_quantity(&mut self, value: u8) -> PyResult<()> {
        self.max_quantity = value;
        Ok(())
    }

    #[getter]
    fn get_is_keyitem(&mut self) -> PyResult<bool> {
        Ok(self.is_keyitem)
    }

    #[setter]
    fn set_is_keyitem(&mut self, value: bool) -> PyResult<()> {
        self.is_keyitem = value;
        Ok(())
    }

    #[getter]
    fn get_description(&mut self) -> PyResult<&String> {
        Ok(&self.description)
    }

    #[setter]
    fn set_description(&mut self, value: String) -> PyResult<()> {
        self.description = value;
        Ok(())
    }
}
