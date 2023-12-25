use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;

use crate::travel_serializer::Bus;

#[derive(Debug)]
pub struct AppState {
    pub bus: Bus,
    pub bus_stops: HashMap<i64, String>,
}

impl AppState {
    pub fn init() -> Self {
        let file = File::open("travel.json").expect("file doesn't find");
        let reader = BufReader::new(file);
        let bus: Bus = serde_json::from_reader(reader).expect("failed to parse json to bus");

        let mut bus_stops: HashMap<i64, String> = HashMap::new();
        for bus in bus.bus_line.iter() {
            for stop in bus.travel.iter() {
                if bus_stops.get(&stop.id).is_none() {
                    bus_stops.insert(stop.id, stop.name.clone());
                }
            }
        }

        Self { bus, bus_stops }
    }
}

#[test]
fn test_app_stat() {
    let app_state = AppState::init();
    println!("{app_state:?}");
}
