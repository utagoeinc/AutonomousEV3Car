#include "Motor.h"
#include <stdlib.h>

class Accelerator{
  public:
    Accelerator(ev3api::Motor* lmotor,
                ev3api::Motor* rmotor);
    void setSpeed(float speed);
    void move();

  private:
    ev3api::Motor* lMotor;
    ev3api::Motor* rMotor;

    float currentSpeed = 0;
    const int MAX_PWM = 100;
};
