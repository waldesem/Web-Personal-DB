use chrono::{NaiveDateTime, NaiveDate};
use diesel::{prelude::*};
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::workplaces)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Staffs {
    pub id: i32,
    pub now_work: i8,
    pub starts: NaiveDate,
    pub finished: Option<NaiveDate>,
    pub workplace: String,
    pub position: String,
    pub address: String,
    pub reason: Option<String>,
    pub created: NaiveDateTime,
    pub person_id: Option<i32>,
}