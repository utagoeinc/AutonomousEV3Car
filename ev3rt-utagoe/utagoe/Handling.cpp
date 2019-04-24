#include "Handling.h"

Handling::Handling (
  ev3api::Motor* motor
):
  mMotor(motor)
{
  init();
}

void Handling::init() {
  // 右に一杯ハンドルを切った状態でモータを初期化
  mMotor->setPWM(30);
  mClock.sleep(500);
  mMotor->reset();
  mClock.sleep(100);
  // 左に一杯ハンドルを切った状態のモータ角位置を取得
  mMotor->setPWM(-30);
  mClock.sleep(500);
  mMotor->setPWM(0);
  LEFT_MAX = mMotor->getCount();

  mClock.sleep(100);
  CENTER = LEFT_MAX/2;
  RANGE = abs(CENTER);

  // 中央にハンドルを戻す
  setAngle(0);
  // move();
}

/**
 *    -1 ......... 0 .......... 1
 * LEFT_MAX ... CENTER ... RIGHT_MAX
 */
void Handling::setAngle(float angle) {
  if (angle > 1) {
    angle = 1;
  }
  if (angle < -1) {
    angle = -1;
  }

  setPosition(CENTER + RANGE*angle);
}

void Handling::setPosition(int32_t position) {
  if (position > RIGHT_MAX) {
    position = RIGHT_MAX;
  }
  if (position < LEFT_MAX) {
    position = LEFT_MAX;
  }

  targetPosition = position;
}

void Handling::move() {
  int32_t currentPosition = mMotor->getCount();
  int32_t diff = currentPosition - targetPosition;

  float coefficient = float(diff)/(LEFT_MAX/10);

  mMotor->setPWM(MAX_PWM * coefficient);
}
