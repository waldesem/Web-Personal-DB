use crate::establish_connection;
use crate::models::user::User;
use crate::types::{Auth, JwToken, Login};
use actix_web::{HttpResponse, Responder, Result, web};
use bcrypt::{DEFAULT_COST, hash, verify};
use chrono::{Duration, Utc};
use diesel::prelude::*;
use jsonwebtoken::{EncodingKey, Header, encode};

pub async fn login(
    action: web::Path<String>,
    req_body: web::Json<Login>,
) -> Result<impl Responder> {
    use crate::schema::users::dsl::*;

    let conn = &mut establish_connection();
    let user = users
        .filter(username.eq(&req_body.username))
        .first::<User>(conn)
        .optional()
        .expect("Ошибка загрузки пользователя");

    match user {
        Some(user) if user.blocked || user.deleted => Ok(HttpResponse::Ok().json(Auth {
            message: "invalid".to_string(),
            access_token: None,
        })),
        Some(user) => {
            // Проверка пароля
            if !verify(&req_body.password, &user.passhash).unwrap_or(false) {
                // Обновление количества попыток
                if user.attempt < 5 {
                    diesel::update(users.filter(id.eq(user.id)))
                        .set(attempt.eq(user.attempt + 1))
                        .execute(conn)
                        .expect("Ошибка обновления попыток");
                } else {
                    diesel::update(users.filter(id.eq(user.id)))
                        .set(blocked.eq(true))
                        .execute(conn)
                        .expect("Ошибка блокировки пользователя");
                }
                return Ok(HttpResponse::Ok().json(Auth {
                    message: "invalid".to_string(),
                    access_token: None,
                }));
            }

            if *action == "update" {
                if let Some(new_pswd) = &req_body.new_pswd {
                    let new_hash = hash(new_pswd, DEFAULT_COST).expect("Ошибка хеширования пароля");
                    diesel::update(users.filter(id.eq(user.id)))
                        .set((
                            passhash.eq(new_hash),
                            pswd_create.eq(Utc::now().naive_utc()),
                            change_pswd.eq(false),
                            attempt.eq(0),
                        ))
                        .execute(conn)
                        .expect("Ошибка обновления пароля");
                    return Ok(HttpResponse::Created().json(Auth {
                        message: "updated".to_string(),
                        access_token: None,
                    }));
                }
            }

            let token = JwToken {
                id: user.id,
                username: user.username,
                fullname: user.fullname,
                role: user.role,
                exp: Utc::now().naive_utc() + Duration::hours(12),
            };
            let secret = std::env::var("JWT_SECRET_KEY").expect("JWT_SECRET_KEY must be set");
            let token_str = encode(
                &Header::default(),
                &token,
                &EncodingKey::from_secret(secret.as_ref()),
            )
            .expect("Ошибка кодирования токена");

            Ok(HttpResponse::Ok().json(Auth {
                message: "success".to_string(),
                access_token: Some(format!("Bearer {}", token_str)),
            }))
        }
        None => Ok(HttpResponse::Ok().json(Auth {
            message: "invalid".to_string(),
            access_token: None,
        })),
    }
}

pub async fn logout() -> impl Responder {
    HttpResponse::Ok().json(Auth {
        message: "success".to_string(),
        access_token: None,
    })
}
