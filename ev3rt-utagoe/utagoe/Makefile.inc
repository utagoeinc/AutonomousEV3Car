APPL_COBJS +=

APPL_CXXOBJS += \
  Handling.o \
  Accelerator.o

SRCLANG := c++

ifdef CONFIG_EV3RT_APPLICATION

# Include libraries
include $(EV3RT_SDK_LIB_DIR)/libcpp-ev3/Makefile

endif

APPL_DIR +=

INCLUDES +=
