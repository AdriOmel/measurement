#include <Arduino.h>
#include "DHT.h"

#include "WiFiS3.h"
#include "WiFiSSLClient.h"
#include "IPAddress.h"

#include "arduino_secrets.h" 

#define DHTPIN 8     

DHT dht(DHTPIN, DHT22);  

// Server parameters
const char* server = "data-measurement.onrender.com"; 
const int port = 443; 
int status = WL_IDLE_STATUS;

char ssid[] = SECRET_SSID;     
char pass[] = SECRET_PASS;       

unsigned long time = 0;
const unsigned long interval = 10000;

WiFiSSLClient client;

void printWiFiStatus();
void send_http_request(String payload);
void read_http_response();
int read_humidity();
float read_temperature();
void send_measurements(float temperatureDHT, int humidity);
void wait_http_response();

void setup() {
  Serial.begin(9600);  
  dht.begin(); 

  while (!Serial) {
    ;
  }

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);

    delay(10000);
  }

  printWiFiStatus();

}

void send_http_request(String payload){
  Serial.println("\nStarting connection to server...");
  Serial.println(server);
  if (client.connect(server, 443)) {
    Serial.println("connected to server");
    client.println("POST /update HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("User-Agent: ArduinoWiFi/1.1");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(payload.length());
    client.println("Connection: close");
    client.println();
    client.println(payload); 
    Serial.println("POST request sent");
  }
}

void printWiFiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void read_http_response()
{
  uint32_t received_data_num = 0;
  while (client.available()) {
    char c = client.read();
    Serial.print(c);
    received_data_num++;
    if(received_data_num % 80 == 0) {
      Serial.println();
    }
  }
}

int read_humidity()
{
  int humidity = dht.readHumidity(); 
  if (isnan(humidity)){
    Serial.println("Error reading humidity data!");
  }
  Serial.println("============");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  return humidity;
}

float read_temperature()
{
  float temperatureDHT = dht.readTemperature(); 
  if (isnan(temperatureDHT)){
    Serial.println("Error reading temperature data!");
  }
  Serial.println("============");
  Serial.print("Temperature: ");
  Serial.print(temperatureDHT);
  Serial.println(" °C");
  return temperatureDHT;
}

void send_measurements(float temperatureDHT, int humidity){
  String payload = "{\"humidity\":" + String(humidity) + ",\"temperature\":" + String(temperatureDHT) + "}";
  send_http_request(payload);
  wait_http_response();
}

void wait_http_response(){
  while(client.connected()){
    read_http_response();
  }
  Serial.println("disconnecting from server.");
  client.stop();
}

void loop() {
  if (millis() - time >= interval){
    time = millis();
    int humidity = read_humidity();
    float temperature = read_temperature();
    send_measurements(temperature, humidity);
  }
}