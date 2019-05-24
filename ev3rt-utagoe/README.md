# EV3RT Control Program
This application controls EV3 hardware.

## Usages
### Simple way
1. Copy sdcard/* into root of your SD card.

1. Insert it into EV3.

1. Turn on your EV3 and run the application.

### Compile by yourself
1. Install EV3RT SDK into your PC.  
    Please refer to [this page](https://github.com/ev3rt-git/ev3rt-hrp2/tree/0301474c6bd8b1fc6a17eef23e995af4edf82e98).

1. Copy utagoe/ under ev3rt-beta7-2-release/hrp2/sdk/workspace/

1. Run the following command on the directory ev3rt-beta7-2-release/hrp2/sdk/workspace/

      ```
      make app=utagoe
      ```

1. Copy ev3rt-beta7-2-release/sdcard/* into your SD card root.

1. Copy ev3rt-beta7-2-release/hrp2/sdk/workspace/app into (YOUR_SD_CARD_ROOT)/ev3rt/apps/

1. Insert it into EV3.

1. Turn on your EV3 and run the application.
