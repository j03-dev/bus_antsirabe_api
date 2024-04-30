#[macro_use]
extern crate rocket;

use std::str::FromStr;

use rocket::serde::json::{json, Json, Value};
use rocket::State;
use rocket_cors::{AllowedHeaders, AllowedMethods, AllowedOrigins, CorsOptions};
use serde::Deserialize;

use app_state::AppState;

use crate::travel_serializer::BustStop;

mod app_state;
mod travel_serializer;

#[derive(Deserialize)]
pub struct Stops {
    pub a: i64,
    pub b: i64,
}

#[post("/travel", format = "json", data = "<stop>")]
fn route(stop: Json<Stops>, state: &State<AppState>) -> Value {
    let mut result: Vec<String> = Vec::new();
    let name_a = state.bus_stops.get(&stop.a);
    let name_b = state.bus_stops.get(&stop.b);
    if let (Some(a), Some(b)) = (name_a, name_b) {
        let stop_a = BustStop {
            id: stop.a,
            name: a.clone(),
        };
        let stop_b = BustStop {
            id: stop.b,
            name: b.clone(),
        };

        result = state
            .bus
            .bus_line
            .iter()
            .filter(|line| line.travel.contains(&stop_a) && line.travel.contains(&stop_b))
            .map(|line| line.name.clone())
            .collect();
    }
    json!(result)
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

#[cfg(test)]
mod testmain {
    use crate::app_state::AppState;
    use crate::Stops;

    use super::route;
    use rocket::serde::json::{json, Json};
    use rocket::State;

    #[test]
    fn test_route() {
        let stop = Stops { a: 8, b: 77 };

        let result_left = route(Json::from(stop), State::from(&AppState::init()));

        let result_right = json!(vec![
            String::from("BUS 4"),
            String::from("BUS 10"),
            String::from("BUS 12"),
            String::from("BUS 16"),
            String::from("BUS 17"),
            String::from("BUS 19")
        ]);

        assert_eq!(result_left, result_right);
    }
}
