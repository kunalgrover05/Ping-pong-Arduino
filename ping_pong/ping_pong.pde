import ddf.minim.spi.*;
import ddf.minim.signals.*;
import ddf.minim.*;
import ddf.minim.analysis.*;
import ddf.minim.ugens.*;
import ddf.minim.effects.*;

import processing.serial.*;


Minim minim;
AudioPlayer s_l,s_r,s_lo,s_h,s_w;//variable name;

Serial myPort;
char val;

int size = 35; 
float xpos, ypos;
float xspeed = random(5, 6); 
float yspeed = random(5, 6);
int p1=0;
int p2=0;

void setup() {
  minim= new Minim(this);
  s_l=minim.loadFile("Alarm Clock.mp3");
  s_r=minim.loadFile("Eas Beep.mp3");
  
  s_w=minim.loadFile("Bleep.mp3");
  s_lo=minim.loadFile("Buzzer2.mp3");
  s_h=minim.loadFile("Robot_blip.mp3");
  
  //  sou.loop();
//  println( Serial.list());
  String portName = "/dev/ttyUSB1";
  
  myPort = new Serial(this, portName, 115200);
  size(800, 600);
  noStroke();
  frameRate(30);
  smooth();
  colorMode(HSB);
  xpos = 40;
  ypos = height/2;
}

void draw() {
  background(0, 0, 0);
  xpos += xspeed;
  ypos += yspeed;
  //print it out in the console
  if (xpos < size/2 ) {
    xpos=width/2;
    xspeed*=-1;
    p2 += 1;
     println("Score"+p1+ " "+p2);
    s_l.pause();
    s_lo.play();
    delay(2000);
    s_lo.pause();       
  } 
  else if ( xpos > width-size/2 ) {
    xpos=width/2;
    xspeed*=-1;
    p1 += 1;
    println("Score "+p1+ " "+p2);
    s_r.pause();
    s_lo.play();
    delay(2000);
    s_lo.pause();
  }
  else if (ypos > height-size/2 || ypos < 0+size/2) {
    yspeed *= -1;
    s_w.play();
  }
  else if (xpos < size*6 && xspeed<0)
  {
    s_l.play();
  } else if (xpos > width-size*6 && xspeed>0) {
    s_r.play();
  } else {
    s_l.pause();
    s_r.pause();
  }
  
  
  ellipse(xpos, ypos, size, size);

  //if (keyPressed) {
  if ( myPort.available() > 0) 
  {  // If data is available,
    val = myPort.readChar();         // read it and store it in val 
    if (val == 'w') {
      //       fill(255,255,0);
      rect (0, 0, 50, height);
      if (xpos<=50) {
        xspeed *= -1;
        yspeed = random(0, 8)-4;
        s_l.pause();
        delay(100);
        s_h.play();
       delay(100); 
      }
    } 
    if ( val == 'e') {
      //       fill(255,255,0);
      rect (width-50, 0, 50, height);
      if (xpos >= width-50) {
           s_r.pause();
           delay(100);
           s_h.play();
          delay(100); 
        xspeed *= -1;
        yspeed = random(0, 8)-4;
        //   }
      }
    }
  }
}



