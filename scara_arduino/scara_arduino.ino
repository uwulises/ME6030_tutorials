#include <Servo.h>
#define pin_L1 5
#define pin_L2 6



Servo L1;
Servo L2;

int poser = 0; // initial position of server
int val;       // initial value of input

String inputString = "";
bool stringComplete = false;
// Homing
void axis_home()
{

  L1.write(0);
  L2.write(0);
}

void setup()
{
  // Attach servos
  Serial.begin(115200);
  L1.attach(pin_L1);
  L2.attach(pin_L2);
  // Homing inicial
  axis_home();
  Serial.println("Ready");
  Serial.println("MOVEAXq1q2");
  Serial.println("q1: 0-180");
  Serial.println("q2: 0-180");
}

void serialEvent()
{
  while (Serial.available())
  {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n')
    {
      stringComplete = true;
    }
  }
}
void move_axis(int servoId, int position)
{
  if (servoId == 1)
  {
    L1.write(position);
  }

  if (servoId == 2)
  {
    L2.write(position);
  }


}
void loop()
{
   if (stringComplete)
  {
    // take the 6 first characters of the string
    // and compare it with "CMDVEL"
    if (inputString.substring(0, 6) == "MOVEAX")
    {
      // take and split the next 6 characters of the string
      int q1 = inputString.substring(6, 9).toInt();
      int q2 = inputString.substring(9, 12).toInt();
      move_axis(1, q1);
      move_axis(2, q2);

    inputString = "";
    stringComplete = false;
  }
}
// move_axis function

}
