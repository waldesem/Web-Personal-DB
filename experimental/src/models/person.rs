use chrono::NaiveDateTime;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use crate::models::user::User;

#[derive(Queryable, Selectable, Serialize, Deserialize, Associations)]
#[diesel(table_name = crate::schema::persons)]
#[diesel(belongs_to(User, foreign_key = user_id))]
pub struct Person {
    pub id: i32,
    pub surname: String,
    pub firstname: String,
    pub patronymic: Option<String>,
    pub birthday: String,
    pub birthplace: String,
    pub citizenship: Option<String>,
    pub dual: Option<String>,
    pub snils: Option<String>,
    pub inn: Option<String>,
    pub marital: Option<String>,
    pub addition: Option<String>,
    pub destination: Option<String>,
    pub created: NaiveDateTime,
    pub editable: bool,
    pub user_id: Option<i32>,
}
