#include "app.h"
#include "Handling.h"
#include "Accelerator.h"
#include <stdio.h>
#include <unistd.h>

// using宣言
using ev3api::Motor;

// Device objects
Motor gSteeringMotor(PORT_A, true, MEDIUM_MOTOR);
Motor gRightWheel(PORT_C, false, LARGE_MOTOR);
Motor gLeftWheel(PORT_B, false, LARGE_MOTOR);

static Handling *gHandling;
static Accelerator *gAccelerator;

static FILE* gBt= ev3_serial_open_file(EV3_SERIAL_BT);

void *__dso_handle = 0;
void *__gxx_personality_v0;

/**
 * EV3システム生成
 */
static void user_system_create() {
    // 初期化
    gHandling = new Handling(&gSteeringMotor);
    gAccelerator = new Accelerator(&gLeftWheel, &gRightWheel);

    // 初期化完了通知
    ev3_led_set_color(LED_ORANGE);
}

/**
 * EV3システム破棄
 */
static void user_system_destroy() {
    gSteeringMotor.reset();
    gRightWheel.reset();
    gLeftWheel.reset();

    delete gHandling;
    delete gAccelerator;

    fclose(gBt);
}

/**
 * 周期ハンドラによるドライバータスクの周期起動
 */
void ev3_cyc_driver(intptr_t exinf) {
    act_tsk(DRIVER_TASK);
}

/**
 *
 */
void ev3_cyc_bluetooth(intptr_t exinf) {
    act_tsk(BT_TASK);
}

/**
 * メインタスク
 */
void main_task(intptr_t unused) {
    user_system_create();  // センサやモータの初期化処理

    // 周期ハンドラ開始
    ev3_sta_cyc(EV3_CYC_DRIVER);
    ev3_sta_cyc(EV3_CYC_BT);

    slp_tsk();  // バックボタンが押されるまで待つ

    // 周期ハンドラ停止
    ev3_stp_cyc(EV3_CYC_DRIVER);
    ev3_stp_cyc(EV3_CYC_BT);
    user_system_destroy();  // 終了処理

    ext_tsk();
}

/**
 * ドライバータスク
 */
void driver_task(intptr_t exinf) {
    if (ev3_button_is_pressed(BACK_BUTTON)) {
        wup_tsk(MAIN_TASK);  // バックボタン押下
    } else {
        drive();
    }

    ext_tsk();
}

/**
 * Bluetoothタスク
 */
 void bluetooth_task(intptr_t exinf) {
   if (gBt != NULL) {
     uint8_t mode = fgetc(gBt);
     uint8_t amount = fgetc(gBt);
     float famount = amountToFloat(amount);

     switch(mode){
       case 'i':
       // forward
       gAccelerator->setSpeed(famount);
       break;

       case 'k':
       // backward
       gAccelerator->setSpeed(-famount);
       break;

       case 'j':
       // left
       gHandling->setAngle(-famount);
       break;

       case 'l':
       // right
       gHandling->setAngle(famount);
       break;

       default:
       gHandling->setAngle(0);
       gAccelerator->setSpeed(0);
     }

     fputc(mode, gBt); /* エコーバック */
     fputc(amount, gBt); /* エコーバック */
   }

   ext_tsk();
 }

/**
 * 車体を動かす
 */
void drive() {
    gHandling->move();
    gAccelerator->move();
}

/**
 * 浮動小数変換
 */
float amountToFloat(uint8_t amount) {
    float retval = 1.0/16;
    char amountStr[] = "";
    unsigned int hex;
    sprintf(amountStr, "%c", amount);
    sscanf(amountStr, "%x", &hex);
    return retval * hex;
}
