#include "Arduino.h"

#include <TimerOne.h>
#include <SD.h>    
#include <SPI.h>

#define greenLED A0
#define limitswitch A1
#define leftbutton A2
#define middlebutton A3
#define rightbutton A4
#define topbutton A5
#define stepperdisable A6
#define SDchipUnselect 4
#define XstepperdirPin 2
#define YstepperdirPin 3
#define Xstepper 9
#define Ystepper 10
#define Wservo 6
#define Pservo 7
#define blueLED 8


const int Xpos = 0;
const int Ypos = 1;
const int Xneg = 1;
const int Yneg = 0;


#define rpm5 3750
#define rpm10 1875
#define rpm15 1250
#define rpm25 750
#define rpm50 375


volatile int Xsteps = 0;
volatile int Ysteps = 0;

int rpmspeed = 0;

int Xglobalposition = 0;
int Yglobalposition = 0;

int Xstepperdir = 0;
int Ystepperdir = 0;

int ServoConstantFrequency = 79999;
int Wservotoolholderheight = 0;
int WservoPenPress = 0;
int WservoPenRelease = 0;
int countingangle = 0;

int TonePosX = 5332;
int TtwoPosX = 7332;
int TthreePosX = 9332;
int TfourPosX = 11332;

int ProbePenHeight = 0;



// Servo Wservo;
// Servo Pservo;

void setup() {
    Serial.begin(9600);
    pinMode(greenLED, OUTPUT);
    pinMode(limitswitch, INPUT);
    pinMode(leftbutton, INPUT);
    pinMode(middlebutton, INPUT);
    pinMode(topbutton, INPUT);
    pinMode(stepperdisable, OUTPUT);
    pinMode(SDchipUnselect, OUTPUT);
    pinMode(Xstepperdir, OUTPUT);
    pinMode(Ystepperdir, OUTPUT);
    pinMode(Xstepper, OUTPUT);
    pinMode(Ystepper, OUTPUT);
    pinMode(Wservo, OUTPUT);
    pinMode(Pservo, OUTPUT);
    pinMode(blueLED, OUTPUT);

    digitalWrite(greenLED, LOW);
    digitalWrite(stepperdisable, LOW);
    digitalWrite(blueLED, LOW);
    digitalWrite(SDchipUnselect, HIGH);
 


    Timer1.initialize(rpm5); // Frequency is configured, but PWM not started yet
    Timer1.attachInterrupt(UpdateStepCounts);// Attach the ISR (it will run even without PWM)
    
    // Wservo.attach(Wservo);
    // Pservo.attach(Pservo);


// Start SD card
  if (!SD.begin(SDchipUnselect)) {
    Serial.println("SD card initialization failed!");
    return;
  }
  Serial.println("SD card initialized.");


}





void loop() {
    // listFiles(SD.open("/"), 0);
    
    FindOrigin();
    delay(2000);
    Timer1.initialize(rpm15);
    processFile("TESTTX~1.TXT");
    digitalWrite(blueLED, HIGH);
    while(1){


  }

}




void listFiles(File dir, int numTabs) {
  while (true) {
    File entry = dir.openNextFile();
    if (!entry) {
      // No more files
      break;
    }
    // Print indentation for nested directory structure
    for (int i = 0; i < numTabs; i++) {
      Serial.print("\t");
    }
    Serial.print(entry.name());
    if (entry.isDirectory()) {
      Serial.println("/");
      // Recursively list files in subdirectory
      listFiles(entry, numTabs + 1);
    } else {
      // For files, print the file size in bytes
      Serial.print("\t\t");
      Serial.println(entry.size(), DEC);
    }
    entry.close();
  }
}



void processFile(const char* filename) {
  File file = SD.open(filename);
  
  if (file) {
    while (file.available()) {

      if (digitalRead(middlebutton) == HIGH) {
        file.close(); // Close the file
        return; // Exit the function early
      }
      String line = file.readStringUntil('\n');

      // Extract values if necessary
      if (line.startsWith("X")) {
        int xIndex = line.indexOf('X') + 1;
        int yIndex = line.indexOf('Y') + 1;

        int Xposition = (xIndex > 0) ? line.substring(xIndex, yIndex - 1).toInt() : 0;
        int Yposition = (yIndex > 0) ? line.substring(yIndex).toInt() : 0;

        Xposition = Xposition * 19;
        Yposition = Yposition * 19;

        stepperinstructor(Xposition, Yposition);
      }
    }
    
    file.close(); // Close the file after processing all lines
  } else {
    Serial.println("Failed to open the file.");
  }
}






void UpdateStepCounts(){
    Xsteps = Xsteps + 1;
    Ysteps = Ysteps + 1;

}

void driveXStepDir(int XstepsToGo, int XdriveDir){
    Xsteps = 0;
    digitalWrite(XstepperdirPin, XdriveDir);
    Timer1.pwm(Xstepper, 128);
    while(Xsteps < XstepsToGo){
        
    }
    Timer1.disablePwm(Xstepper);
    
}

void driveYStepDir(int YstepsToGo, int YdriveDir){
    Ysteps = 0;
    digitalWrite(YstepperdirPin, YdriveDir);
    Timer1.pwm(Ystepper, 128);
    while(Ysteps < YstepsToGo){
      
    }
    Timer1.disablePwm(Ystepper);
    
}


void driveStepperstogether(int XstepsToGo, int XdriveDir, int YstepsToGo, int YdriveDir){
    Xsteps = 0;
    Ysteps = 0;
    digitalWrite(XstepperdirPin, XdriveDir);
    digitalWrite(YstepperdirPin, YdriveDir);
    Timer1.pwm(Xstepper, 128);
    Timer1.pwm(Ystepper, 128);
    while(Xsteps < XstepsToGo || Ysteps < YstepsToGo){

        if(Xsteps > XstepsToGo){
            Timer1.disablePwm(Xstepper);
        }
        
        
        if(Ysteps > YstepsToGo){
            Timer1.disablePwm(Ystepper);
        }
        
        

    }
    Timer1.disablePwm(Xstepper);
    Timer1.disablePwm(Ystepper);
    
}



void stepperinstructor(int Xnextposition, int Ynextposition){
    
    int Xdistance = Xnextposition - Xglobalposition;
    int Ydistance = Ynextposition - Yglobalposition;
    int XstepsToGo = abs(Xdistance);
    int YstepsToGo = abs(Ydistance);
    int XdriveDir;
    int YdriveDir;
    if(Xdistance > 0){
        XdriveDir = Xpos;
        Xglobalposition = Xglobalposition + Xdistance;
    }
    else{
        XdriveDir = Xneg;
        Xglobalposition = Xglobalposition + Xdistance;
    }
    
    if(Ydistance > 0){
        YdriveDir = Ypos;
        Yglobalposition = Yglobalposition + Ydistance;
    }
    else{
        YdriveDir = Yneg;
        Yglobalposition = Yglobalposition + Ydistance;
    }
    
    driveStepperstogether(XstepsToGo,XdriveDir,YstepsToGo,YdriveDir);
}


void FindOrigin(){
    int SwitchUnpressed = digitalRead(limitswitch);
    digitalWrite(YstepperdirPin, Yneg);
    Timer1.pwm(Ystepper, 128);
    while(SwitchUnpressed == 1){
        SwitchUnpressed = digitalRead(limitswitch);
    }
    driveYStepDir(900, Ypos);
    Timer1.disablePwm(Ystepper);
    delay(500);

    digitalWrite(XstepperdirPin, Xneg);
    Timer1.pwm(Xstepper, 128);
    SwitchUnpressed = digitalRead(limitswitch);
    while(SwitchUnpressed == 1){
        SwitchUnpressed = digitalRead(limitswitch);
    }
    driveXStepDir(400, Xpos);
    Timer1.disablePwm(Xstepper);

    Timer1.initialize(rpm15);
    driveStepperstogether(0, Xpos, 7000, Ypos);
    driveStepperstogether(400, Xneg, 0, Ypos);
    Xglobalposition = 0;
    Yglobalposition = 0;
    
    
}

