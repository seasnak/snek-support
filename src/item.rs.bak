use pyo3::prelude::*;

#[pyclass]
struct Item {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub description: String,
    pub quantity: i8,
    pub is_infinite: bool,
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
            name: item_name,
            description: String::new(),
            quantity: num_items,
            is_infinite: false,
        }
    }

    #[getter]
    fn get_quantity(&mut self) -> PyResult<i8> {
        Ok(self.quantity)
    }

    #[setter]
    fn set_quantity(&mut self, value: i8) -> PyResult<()> {
        self.quantity = value;
        Ok(())
    }

    #[getter]
    fn get_is_infinite(&mut self) -> PyResult<bool> {
        Ok(self.is_infinite)
    }

    #[setter]
    fn set_is_infinite(&mut self, value: bool) -> PyResult<()> {
        self.is_infinite = value;
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
