cmake_minimum_required(VERSION 3.12)

project(blink_project)

set(PICO_SDK_PATH ../pico-sdk)

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

add_executable(blink
    blink.c
)

pico_sdk_init()

# Add correct architecture options
target_compile_definitions(blink PRIVATE
    PICO_TARGET_M33
)

target_compile_options(blink PRIVATE
    -mcpu=cortex-m33
    -mthumb
    -mfloat-abi=hard
    -mfpu=fpv5-sp-d16
)

target_link_libraries(blink pico_stdlib)

pico_add_extra_outputs(blink)
