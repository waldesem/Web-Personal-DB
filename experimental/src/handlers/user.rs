use actix_web::{HttpResponse, Responder, web};

pub async fn get_users() -> impl Responder {
    HttpResponse::Ok().body("Users!")
}

pub async fn post_user(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

pub async fn edit_user(id: web::Path<u32>, req_body: String) -> impl Responder {
    let user_id = id.into_inner();
    if user_id == 0 {
        HttpResponse::Ok().body("No user!")
    } else {
        HttpResponse::Ok().json(req_body)
    }
}
