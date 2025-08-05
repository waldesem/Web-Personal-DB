use diesel::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Serialize, Deserialize)]
#[diesel(table_name = crate::schema::users)]
pub struct User {
    pub id: i32,
    pub fullname: String,
    pub username: String,
    pub email: String,
    pub created: String,
    pub passhash: String,
    pub pswd_create: String,
    pub change_pswd: bool,
    pub blocked: bool,
    pub deleted: bool,
    pub attempt: Option<i32>,
    pub role: String,
}
