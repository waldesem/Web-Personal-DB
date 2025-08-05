use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::person::Person;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::checks)]
#[diesel(belongs_to(Person, foreign_key = person_id))]
pub struct Staffs {
    pub id: i32,
    pub workplace: Option<String>,
    pub document: Option<String>,
    pub inn: Option<String>,
    pub debt: Option<String>,
    pub bankruptcy: Option<String>,
    pub bki: Option<String>,
    pub courts: Option<String>,
    pub affilation: Option<String>,
    pub terrorist: Option<String>,
    pub mvd: Option<String>,
    pub internet: Option<String>,
    pub cronos: Option<String>,
    pub cros: Option<String>,
    pub addition: Option<String>,
    pub comment: Option<String>,
    pub conclusion: Option<String>,
    pub created: NaiveDateTime,
    pub person_id: Option<i32>,
}