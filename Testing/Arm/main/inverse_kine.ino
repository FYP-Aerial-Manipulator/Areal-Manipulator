#include <math.h>

// CALCULATING FOUR THREE ANGLES
void determineAngles() {
  float pos_ang[3];  // STORING FIRST THREE ANGLES IN RADIAN
  float Xv = dest[0];
  float Yv = dest[1];
  float Zv = dest[2];

  pos_ang[0] = atan(Yv / Xv);

  // CALCULATION OF OC
  // for (int ii = 0; ii < 3; ii++)
  //   Oc[ii] = dest[ii];
  // if (case_vert)
  //   Oc[2] += 17.5; 
  // else
  //   Oc[0] -= 17.5*cos(pos_ang[0]), Oc[1] -= 17.5*sin(pos_ang[0]);

  float l1 = 10.5, l2 = 20.5;
  // float Xc = Oc[0], Yc = Oc[1], Zc = Oc[2] - 7;
  float r = sqrt(pow(Xv, 2) + pow(Yv, 2) + pow(Zv, 2));

  pos_ang[2] = acos((pow(r, 2) - pow(l1, 2) - pow(l2, 2)) / (2 * l1 * l2));
  pos_ang[1] = M_PI / 2 - atan(Zv / sqrt(pow(Xv, 2) + pow(Yv, 2))) - acos((pow(r, 2) + pow(l1, 2) - pow(l2, 2))/(2*l1*r));


  config_inv[0] = angleToDegrees(pos_ang[0]);
  config_inv[1] = angleToDegrees(pos_ang[1]);
  config_inv[2] = angleToDegrees(pos_ang[2]);
  config_inv[3] = 90;

  // if (case_vert) config_inv[3] = 180 - config_inv[1] - config_inv[2], config_inv[4] = 0;
  // else config_inv[1]-=37, config_inv[2]-=180, config_inv[3] = 90 - config_inv[1] - config_inv[2], config_inv[4] = 90;
  // config_inv[5] = 130;

  // COMPENSATION FOR MOTOR ASSEMBLY
  // config_inv[0] += 90;
  // config_inv[2] += 94;

  config_inv[0] += 90;
  config_inv[1] = 90 - config_inv[1];
  config_inv[2] = 180 - config_inv[2];
}

void inverseCalculation() {
  Serial.println("\ninverse calculation start:...");
  determineAngles();
  Serial.print("CALCULATED: \t");
  configVisualizer(config_inv);
}