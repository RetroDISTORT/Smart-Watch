//C:\Users\RDGC_\OneDrive\Documents\College Documents\Arduino //ORIGINAL SKETCHBOOK LOCATION
/*
 * To add the libraries go to Sketch>Add File...
 */


#include "Arduino.h"
#include "WiFi.h"
#include "C:\Users\RDGC_\OneDrive\Documents\Projects\ArduinoInterpreter\Arduino OS\ESP32-audioI2S-master\src\Audio.h"
#include "SD.h"
#include "FS.h"

// Digital I/O used
#define SD_CS          5
#define SPI_MOSI      23
#define SPI_MISO      19
#define SPI_SCK       18
/*/BOARD
#define I2S_DOUT      21
#define I2S_BCLK      26
#define I2S_LRC       25
//WATCH*/
#define I2S_BCLK      26
#define I2S_LRC       25
#define I2S_DOUT      13

Audio audio;

String ssid ="Rwifi"; //"FRCCStudent";//
String password = "RD123456789"; //"";

void setup() {
  pinMode(33, OUTPUT);
  digitalWrite(33, HIGH); 
  delay(500);
    //SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    Serial.begin(115200);
     Serial.println("DEBUG 1");
    //SD.begin(SD_CS);
    WiFi.disconnect();
    Serial.println("DEBUG 2");
    WiFi.mode(WIFI_STA);
    Serial.println("DEBUG 3");
    WiFi.begin(ssid.c_str(), password.c_str());
    Serial.println("DEBUG 4");
    while (WiFi.status() != WL_CONNECTED) delay(1500);
    Serial.println("DEBUG 5");
    audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
    audio.setVolume(15); // 0...21

    //audio.connecttoSD("/320k_test.mp3");
    //audio.connecttohost("www.wdr.de/wdrlive/media/einslive.m3u");
    //audio.connecttohost("dg-ais-eco-http-fra-eco-cdn.cast.addradio.de/hellwegradio/west/mp3/high");
    audio.connecttohost("fischkopp.stream.laut.fm/fischkopp");
    //audio.connecttospeech("Im tired of this class", "de");
}

void loop()
{
    audio.loop();
}

// optional
void audio_info(const char *info){
    Serial.print("info        "); Serial.println(info);
}
void audio_id3data(const char *info){  //id3 metadata
    Serial.print("id3data     ");Serial.println(info);
}
void audio_eof_mp3(const char *info){  //end of file
    Serial.print("eof_mp3     ");Serial.println(info);
}
void audio_showstation(const char *info){
    Serial.print("station     ");Serial.println(info);
}
void audio_showstreaminfo(const char *info){
    Serial.print("streaminfo  ");Serial.println(info);
}
void audio_showstreamtitle(const char *info){
    Serial.print("streamtitle ");Serial.println(info);
}
void audio_bitrate(const char *info){
    Serial.print("bitrate     ");Serial.println(info);
}
void audio_commercial(const char *info){  //duration in sec
    Serial.print("commercial  ");Serial.println(info);
}
void audio_icyurl(const char *info){  //homepage
    Serial.print("icyurl      ");Serial.println(info);
}
void audio_lasthost(const char *info){  //stream URL played
    Serial.print("lasthost    ");Serial.println(info);
}
void audio_eof_speech(const char *info){
    Serial.print("eof_speech  ");Serial.println(info);
}
