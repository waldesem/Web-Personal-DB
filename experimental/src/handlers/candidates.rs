use actix_web::{HttpResponse, Responder, web};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct Info {
    search: String,
    per_page: u32,
    total: u32,
}

pub async fn candidates(query: web::Query<Info>) -> impl Responder {
    if query.search.is_empty() {
        return HttpResponse::Ok().body("No search query!");
    }
    if query.total == 0 {
        if query.per_page == 0 {
            return HttpResponse::Ok().body("No candidates!");
        }
    }
    if query.per_page == 0 {
        if query.total == 0 {
            return HttpResponse::Ok().body("No candidates!");
        }
    }
    HttpResponse::Ok().body("Candidates!")
}
