use rocket::serde::{Deserialize, Serialize};
use serde::{Deserializer, Serializer};

#[derive(Debug, Clone, PartialOrd, PartialEq)]
pub struct BustStop {
    pub id: i64,
    pub name: String,
}

impl Serialize for BustStop {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: Serializer,
    {
        #[derive(Serialize)]
        struct LowercaseBustStop<'a> {
            id: i64,
            #[serde(serialize_with = "serialize_lowercase")]
            name: &'a str,
        }

        fn serialize_lowercase<S>(value: &&str, serializer: S) -> Result<S::Ok, S::Error>
            where
                S: Serializer,
        {
            value.to_lowercase().serialize(serializer)
        }

        let lowercase_bust_stop = LowercaseBustStop {
            id: self.id,
            name: &self.name,
        };

        lowercase_bust_stop.serialize(serializer)
    }
}

impl<'de> Deserialize<'de> for BustStop {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: Deserializer<'de>,
    {
        #[derive(Deserialize)]
        struct LowercaseBustStop {
            id: i64,
            #[serde(deserialize_with = "deserialize_lowercase")]
            name: String,
        }

        fn deserialize_lowercase<'de, D>(deserializer: D) -> Result<String, D::Error>
            where
                D: Deserializer<'de>,
        {
            let s: String = Deserialize::deserialize(deserializer)?;
            Ok(s.to_lowercase())
        }

        let lowercase_bust_stop: LowercaseBustStop = Deserialize::deserialize(deserializer)?;

        Ok(BustStop {
            id: lowercase_bust_stop.id,
            name: lowercase_bust_stop.name,
        })
    }
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

