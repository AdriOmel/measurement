CREATE TABLE Sensors (
    id serial PRIMARY KEY,
	mac_adress      text,
	sensor_type text,
	correction float4,
	sensor_location text,
	units text
);
	
CREATE TABLE Measurments (
	id serial PRIMARY KEY,
    sensor_id     int,
	sensor_value float4,
    datetime        timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,	
	correction float4,
    FOREIGN KEY (sensor_id) REFERENCES Sensors (id)
)
;