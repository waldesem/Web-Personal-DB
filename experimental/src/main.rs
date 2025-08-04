use actix_files as fs;
use actix_web::{App, HttpRequest, HttpServer, Result, get};
use std::path::PathBuf;
use experimental::routes;

#[get("/")]
async fn index(req: HttpRequest) -> Result<fs::NamedFile> {
    let path: PathBuf = req.match_info().query("filename").parse().unwrap();
    Ok(fs::NamedFile::open(path)?)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .configure(routes::configure)
            .service(index)
            .service(fs::Files::new("/static", ".").use_last_modified(true))
    })
    .bind(("127.0.0.1", 5000))?
    .run()
    .await
}
