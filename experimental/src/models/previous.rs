use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::previous)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Previous {
    pub id: i32,
    pub surname: String,
    pub firstname: String,
    pub patronymic: Option<String>,
    pub changed: String,
    pub reason: Option<String>,
    pub created: NaiveDateTime,
    pub person_id: i32,
}