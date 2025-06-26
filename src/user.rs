use pyo3::prelude::*;

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
