// Includes
#include <math.h>
#include <Servo.h>


#define MID_DELAY 100
#define J_COUNT 4
#define STEP_ANGLE 1
#define TOLERANCE 1
#define M_PI 3.14159265358979323846
#define angleToDegrees(val) (val * 180 / 3.14159265358979323846)

// CLASS FOR CONTROLLING THE ROBOTIC ARM
class roboticArm {
  Servo JOINTS[J_COUNT];
private:
  int cur_pos[J_COUNT];
  int exp_pos[J_COUNT];
public:
  roboticArm(int* init_pos, int* pins);
  void setConfiguration(int* exp_pos_);
  bool approach(int joint);
  bool moveArm();
  void visualizeConfiguration();
};

void configVisualizer(int* config);
void inverseCalculation(); // true - Link 5 Vertical

// GLOBAL VARIABLES
int config_buf[J_COUNT];
int config_inv[J_COUNT];
float ang_offset[J_COUNT];
float dest[3];



void setup() {
  Serial.begin(9600);

  // INITIALIZING THE ARM
  int init_config[J_COUNT] = { 90, 90, 120, 90 };
  int pins_[J_COUNT] = { 5, 6, 9, 10 };
  ang_offset[0] = 90, ang_offset[1] = 90, ang_offset[2] = 90, ang_offset[3] = 130;


  roboticArm RA(init_config, pins_);

  for (int j = 0; j < J_COUNT; j++)
    config_buf[j] = init_config[j];

  // Inverse Kinematic Calculation
  dest[0] = 22, dest[1] = 0, dest[2] = 0;
  // inverseCalculation();

  dest[0] = 18.7, dest[1] = -18.7, dest[2] = 8.6;
  // inverseCalculation();

  // READING THE SERIAL MONITOR
  while (true)
    if (Serial.available() > 0) {
      // READING THE SERIAL MONITOR FOR SETTING ANGLE
      String inputString = Serial.readStringUntil('\n');
      String indexString = inputString.substring(0, 1);
      int index = indexString.toInt();

///////////////////////// FORWARD KINEMATICS ///////////////////////////////////////////////////
/*
      if (index < 5) {                                  // SETTING THE POSITION ONE BY ONE
        String valueString = inputString.substring(2);  // Skip ": "
        int value = valueString.toInt();
        config_buf[index - 1] = value;
      }else if (index == 5) {  // VISUALIZING THE CONFIG BUFFER
        Serial.print("\nNEXT :\t\t");
        configVisualizer(config_buf);
      } else if (index == 6) {
        RA.visualizeConfiguration();
      } else {
        RA.setConfiguration(config_buf);
        while (!RA.moveArm())
          delay(MID_DELAY);        
      }
    }
*/
//////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////// INVERSE KINEMATICS ////////////////////////////////////////////////

      if (index < 4) {                                  // SETTING THE POSITION ONE BY ONE
        String valueString = inputString.substring(2);  // Skip ": "
        int value = valueString.toInt();
        dest[index - 1] = value;
      }else if (index == 4) {  // VISUALIZING THE CONFIG BUFFER
        inverseCalculation();
      } else if (index == 5) {
        RA.visualizeConfiguration();
      } else {
        RA.setConfiguration(config_inv);
        while (!RA.moveArm())
          delay(MID_DELAY);        
      }
    }
/////////////////////////////////////////////////////////////////////////////////////////////
}

void loop() {
  // DUMMY FUNCTION
}



     

