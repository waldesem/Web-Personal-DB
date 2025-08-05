use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::contacts)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Staffs {
    pub id: i32,
    pub view: String,
    pub contact: String,
    pub created: NaiveDateTime,
    pub person_id: Option<i32>,
}