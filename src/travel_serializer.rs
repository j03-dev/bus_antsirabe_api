use rocket::serde::{Deserialize, Serialize};
use serde::{Deserializer, Serializer};

fn serialize_lowercase<S>(value: &str, serializer: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    value.to_lowercase().serialize(serializer)
}

fn deserialize_lowercase<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    let s: String = Deserialize::deserialize(deserializer)?;
    Ok(s.to_lowercase())
}

#[derive(Debug, Clone, PartialOrd, PartialEq, Serialize, Deserialize)]
pub struct BustStop {
    pub id: i64,
    #[serde(
        serialize_with = "serialize_lowercase",
        deserialize_with = "deserialize_lowercase"
    )]
    pub name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Line {
    pub id: i64,
    pub name: String,
    pub primus: BustStop,
    pub terminus: BustStop,
    pub travel: Vec<BustStop>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Bus {
    #[serde(rename = "busLine")]
    pub bus_line: Vec<Line>,
}

#[test]
fn test_lower_case_d_s() {
    let bus_stop_left = BustStop {
        id: 1,
        name: "lowercase".into(),
    };

    let json_d = r#"{"id": 1, "name": "Lowercase"}"#;
    let bus_stop_right =
        serde_json::from_str::<BustStop>(json_d).expect("failed to parse this json to bus struct");

    assert_eq!(bus_stop_left, bus_stop_right);
}
