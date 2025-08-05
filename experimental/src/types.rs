use chrono::NaiveDateTime;
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct BaseResponse {
    pub message: String,
}

#[derive(Serialize)]
pub struct Auth {
    pub message: String,
    pub access_token: Option<String>,
}

#[derive(Deserialize)]
pub struct Login {
    pub username: String,
    pub password: String,
    pub new_pswd: Option<String>,
}

#[derive(Serialize, Deserialize)]
pub struct JwToken {
    pub id: i32,
    pub username: String,
    pub fullname: String,
    pub role: String,
    pub exp: NaiveDateTime,
}