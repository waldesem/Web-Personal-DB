use actix_web::{HttpResponse, Responder, web};

pub async fn get_item(item: String, id: web::Path<u32>) -> impl Responder {
    HttpResponse::Ok().body(format!("{} with id {}", item, id))
}

pub async fn post_item(item: String, id: web::Path<u32>, req_body: String) -> impl Responder {
    HttpResponse::Ok().body(format!("{} with {} id {}", item, req_body, id))
}

pub async fn delete_item(item: String, id: web::Path<u32>) -> impl Responder {
    HttpResponse::Ok().body(format!("{} with id {}", item, id))
}