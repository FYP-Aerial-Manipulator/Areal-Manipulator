// FUNCTION TO INITIALIZE THE CONFIGURATION
roboticArm::roboticArm(int* init_pos, int* pins) {
  for (int j = 0; j < J_COUNT; j++) {
    cur_pos[j] = init_pos[j];
    JOINTS[j].attach(pins[j]);
    JOINTS[j].write(init_pos[j]);
  }
}

// FUNCTION TO MAKE EACH JOINT APPROACH THE EXPECTED POSITION
bool roboticArm::approach(int arm) {
  if (fabs(cur_pos[arm] - exp_pos[arm]) < TOLERANCE)
    return true;
  if (cur_pos[arm] < exp_pos[arm])
    cur_pos[arm] += STEP_ANGLE;
  else
    cur_pos[arm] -= STEP_ANGLE;
  JOINTS[arm].write(cur_pos[arm]);
  return false;
}

// FUNCTION TO SET THE EXPECTED CONFIGURATION
void roboticArm::setConfiguration(int* exp_pos_) {
  for (int j = 0; j < J_COUNT; j++)
    exp_pos[j] = exp_pos_[j];
}

// FUNCTION TO MOVE THE ARM ACCORDINGLY
bool roboticArm::moveArm() {
  bool reached_tag = true;
  for (int jj = 0; jj < J_COUNT; jj++)
    if (!approach(jj))
      reached_tag = false;
  return reached_tag;
}

void roboticArm::visualizeConfiguration() {
  Serial.print("\nCURRENT: \t");
  configVisualizer(cur_pos);
return;
}

void configVisualizer(int* config) {
  for (int j = 0; j < J_COUNT; j++) {
    Serial.print("angle "), Serial.print(j + 1), Serial.print(": ");
    Serial.print(config[j]), Serial.print("\t");
  }}