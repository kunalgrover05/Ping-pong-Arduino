void setup()
{
  Serial.begin(115200);    
}

void loop()
{
  int sensorValue_1=analogRead(A0); 
  int sensorValue_2=analogRead(A3);


  if (sensorValue_1==1023 && sensorValue_2<1023) {
    for(int i=0;i<5;++i)    
      Serial.println("w");
  } 
  if (sensorValue_1<1023 && sensorValue_2==1023) { 
    for(int i=0;i<5;++i)    	    
      Serial.println("e");
  }
  delay(300);

}


