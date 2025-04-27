cmake_minimum_required(VERSION 3.13)


# You must explicitly set where the pico-sdk is
set(PICO_SDK_PATH ${PICO_SDK_PATH})
set(PICO_BOARD pico2_w CACHE STRING "Board type")

# Include the SDK
include(${PICO_SDK_PATH}/pico_sdk_init.cmake)
include(pico_sdk_import.cmake)

project(blink C CXX ASM)
# Initialize the SDK
pico_sdk_init()

# Add the executable
add_executable(blink
    blink.c
)

# Tell CMake/GCC we are using Cortex-M33 (not M0+)
target_compile_options(blink PRIVATE
    -mcpu=cortex-m33
    -mthumb
    -mfloat-abi=hard
    -mfpu=fpv5-sp-d16
)

# Define for your code if needed
target_compile_definitions(blink PRIVATE
    PICO_TARGET_RP2350
)

# Link the standard Pico libraries
target_link_libraries(blink pico_stdlib)

# Create binary, hex, uf2 files
pico_add_extra_outputs(blink)
