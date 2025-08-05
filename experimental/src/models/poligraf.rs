use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::poligrafs)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Staffs {
    pub id: i32,
    pub theme: String,
    pub results: String,
    pub conclusion: String,
    pub created: NaiveDateTime,
    pub person_id: Option<i32>,
}