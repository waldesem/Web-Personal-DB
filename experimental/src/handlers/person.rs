use actix_web::{HttpResponse, Responder, web};

pub async fn get_person(id: web::Path<u32>) -> impl Responder {
    HttpResponse::Ok().body(format!("person with id {}", id))
}

pub async fn post_person(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(format!("person with id {}", req_body))
}

pub async fn delete_person(id: web::Path<u32>) -> impl Responder {
    match id.into_inner() {
        1 => HttpResponse::Ok().body("person deleted"),
        _ => HttpResponse::NotFound().body("person not found"),
    }
}