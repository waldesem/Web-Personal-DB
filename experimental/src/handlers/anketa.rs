use actix_web::{HttpResponse, Responder, web};

pub async fn self_id(id: web::Path<u32>) -> impl Responder {
    HttpResponse::Ok().body(format!("person with id {}", id))
}

pub async fn files(id: web::Path<u32>) -> impl Responder {
    HttpResponse::Ok().body(format!("person with id {}", id))
}

pub async fn json_api() -> impl Responder {
    HttpResponse::Ok()
}
