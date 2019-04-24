#include "Motor.h"
#include <Clock.h>
#include <stdlib.h>

class Handling{
  public:
    Handling(ev3api::Motor* motor);
    void setAngle(float angle); // -1.0(LEFT_MAX) to 1.0(RIGHT_MAX)
    void move();

  private:
    ev3api::Motor* mMotor;
    ev3api::Clock mClock = ev3api::Clock();

    int32_t LEFT_MAX = 0;
    const int32_t RIGHT_MAX = 0;
    int32_t CENTER = 0;
    int32_t RANGE = 0;

    const int MAX_PWM = 100;

    int32_t targetPosition = 0;

    void init();
    void setPosition(int32_t position);
};
