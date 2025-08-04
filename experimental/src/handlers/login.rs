use actix_web::{HttpResponse, Responder, web};

pub async fn login(action: web::Path<String>, req_body: String) -> impl Responder {
    match action.as_str() {
        "login" => HttpResponse::Ok().body(req_body),
        "register" => HttpResponse::Ok().body("Register"),
        _ => HttpResponse::Ok().body("Unknown action"),
    }
}
