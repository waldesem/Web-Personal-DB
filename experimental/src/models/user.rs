use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Serialize, Deserialize)]
#[diesel(table_name = crate::schema::users)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
pub struct User {
    pub id: i32,
    pub fullname: String,
    pub username: String,
    pub email: String,
    pub created: NaiveDateTime,
    pub passhash: String,
    pub pswd_create: NaiveDateTime,
    pub change_pswd: bool,
    pub blocked: bool,
    pub deleted: bool,
    pub attempt: i32,
    pub role: String,
}
