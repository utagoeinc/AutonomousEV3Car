#include "Accelerator.h"

Accelerator::Accelerator (
  ev3api::Motor* lmotor,
  ev3api::Motor* rmotor
):
  lMotor(lmotor),
  rMotor(rmotor)
{
}

/**
 *       -1 ....... 0 ........ 1
 * BACKWARD_MAX ... STOP ... FORWARD_MAX
 */
void Accelerator::setSpeed(float speed) {
  if (speed > 1) {
    speed = 1;
  }
  if (speed < -1) {
    speed = -1;
  }

  currentSpeed = -speed;
}

void Accelerator::move() {
  lMotor->setPWM(MAX_PWM * currentSpeed);
  rMotor->setPWM(MAX_PWM * currentSpeed);
}
