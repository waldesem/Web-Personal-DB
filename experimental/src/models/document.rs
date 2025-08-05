use chrono::{NaiveDateTime, NaiveDate};
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::documents)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Staffs {
    pub id: i32,
    pub view: Option<String>,
    pub series: Option<String>,
    pub digits: String,
    pub issue: NaiveDate,
    pub agency: Option<String>,
    pub created: NaiveDateTime,
    pub person_id: Option<i32>,
}