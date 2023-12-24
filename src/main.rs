#[macro_use]
extern crate rocket;

use std::str::FromStr;

use rocket::serde::json::{json, Json, Value};
use rocket::State;
use rocket_cors::{AllowedHeaders, AllowedMethods, AllowedOrigins, CorsOptions};
use serde::Deserialize;

use app_state::AppState;

use crate::travel_serializer::BustStop;

mod travel_serializer;
mod app_state;

#[derive(Deserialize)]
pub struct Credential {
    pub a: BustStop,
    pub b: BustStop,
}

#[post("/travel", format = "json", data = "<credential>")]
fn route(credential: Json<Credential>, state: &State<AppState>) -> Value {
    let res: Vec<_> = state.bus.bus_line
        .iter()
        .filter(|bus| bus.travel.contains(&credential.a) && bus.travel.contains(&credential.b))
        .map(|item| item.name.clone())
        .collect();
    json!(res)
}

#[get("/travel")]
fn travel(state: &State<AppState>) -> Value {
    json!(state.bus_stops)
}

#[launch]
async fn rocket() -> _ {
    let allowed_origins = AllowedOrigins::all();

    let allowed_methods: AllowedMethods = ["Get", "Post"]
        .iter()
        .map(|s| FromStr::from_str(s).unwrap())
        .collect();

    let cors = CorsOptions {
        allowed_origins,
        allowed_methods,
        allowed_headers: AllowedHeaders::all(),
        allow_credentials: true,
        ..Default::default()
    }
        .to_cors()
        .expect("something is wrong on cors file");

    rocket::build()
        .mount("/api", routes![travel, route])
        .manage(AppState::init())
        .attach(cors)
}
