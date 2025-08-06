use crate::establish_connection;
use crate::schema::{persons, users};
use actix_web::{HttpResponse, Responder, Result, web};
use chrono::{NaiveDate, NaiveDateTime};
use diesel::dsl::sql;
use diesel::{prelude::*, sql_types::Text};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct Index {
    search: Option<String>,
    per_page: u32,
    page: u32,
}

#[derive(Serialize)]
struct PersonResponse {
    id: i32,
    fullname: String,
    birthday: NaiveDate,
    editable: bool,
    created: NaiveDateTime,
    username: String,
}

pub async fn get_index(query: web::Query<Index>) -> Result<impl Responder> {
    let conn = &mut establish_connection();

    let mut stmt = persons::table
        .inner_join(users::table.on(users::id.eq(persons::user_id)))
        .select((
            persons::id,
            sql::<Text>("CONCAT(persons.surname, ' ', persons.firstname, ' ', COALESCE(persons.patronymic, '')) as fullname"),
            persons::birthday,
            persons::editable,
            persons::created,
            users::fullname,
        ));

    // if let Some(search) = &query.search {
    //     let parts: Vec<&str> = search.split_whitespace().collect();
    //     if parts.len() >= 1 {
    //         stmt = stmt.filter(persons::surname.eq(parts[0]));
    //     }
    //     if parts.len() >= 2 {
    //         stmt = stmt.filter(persons::firstname.eq(parts[1]));
    //     }
    //     if parts.len() >= 3 {
    //         stmt = stmt.filter(persons::patronymic.eq(parts[2]));
    //     }
    // }

    let offset = (query.page - 1) * query.per_page;
    let limit = query.per_page;

    // Выполнение запроса
    let results: Vec<(i32, String, NaiveDate, bool, NaiveDateTime, String)> = stmt
        .order(persons::id.desc())
        .offset(offset.into())
        .limit(limit.into())
        .get_results(conn)?;

    // Формирование ответа
    let response: Vec<PersonResponse> = results
        .into_iter()
        .map(
            |(id, fullname, birthday, editable, created, username)| PersonResponse {
                id,
                fullname,
                birthday,
                editable,
                created,
                username,
            },
        )
        .collect();

    Ok(HttpResponse::Ok().json(response))
}
