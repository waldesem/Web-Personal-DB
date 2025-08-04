use actix_web::web;

use crate::handlers::anketa::{files, json_api, self_id};
use crate::handlers::candidates::candidates;
use crate::handlers::items::{get_item, post_item, delete_item};
use crate::handlers::login::login;
use crate::handlers::person::{get_person, post_person, delete_person};
use crate::handlers::user::{get_users, post_user, edit_user};

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/route")
            .route("/index", web::get().to(candidates))
            .route("/users", web::get().to(get_users))
            .route("/user", web::post().to(post_user))
            .route("/user/{id}", web::get().to(edit_user))
            .route("/self/{id}", web::get().to(self_id))
            .route("/files{id}", web::post().to(files))
            .route("/api/json", web::get().to(json_api)) 
            .route("/person", web::post().to(post_person))
            .route("/person/{id}", web::get().to(get_person))
            .route("/person/{id}", web::delete().to(delete_person))
            .route("/{item}/{id}", web::get().to(get_item))
            .route("/{item}/{id}", web::post().to(post_item))
            .route("/{item}/{id}", web::delete().to(delete_item))
            .service(web::scope("/auth").route("/{action}", web::post().to(login))),
    );
}
