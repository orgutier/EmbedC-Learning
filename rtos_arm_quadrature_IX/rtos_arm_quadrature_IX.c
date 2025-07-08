#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "hardware/pwm.h"

// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define I2C_PORT i2c0
#define I2C_SDA 6
#define I2C_SCL 7
#define i2c_buffer_len 10

#define SERVO1 28   // Slice 1, Channel A
#define SERVO2 27   // Slice 1, Channel B
#define SERVO3 26   // Slice 2, Channel A
#define SERVO4 22   // Slice 2, Channel B
#define SERVO5 21   // Slice 3, Channel A
#define SERVO6 20   // Slice 3, Channel B


// Initialize one PWM channel
void setup_servo_pwm(uint gpio, float clk_div, uint16_t wrap) {
    gpio_set_function(gpio, GPIO_FUNC_PWM);
    uint slice = pwm_gpio_to_slice_num(gpio);
    pwm_set_wrap(slice, wrap);
    pwm_set_clkdiv(slice, clk_div);
    pwm_set_enabled(slice, true);
}

void set_servo_pulse(uint gpio, uint16_t level) {
    pwm_set_gpio_level(gpio, level);
}

// Converts microseconds to PWM compare level
uint16_t us_to_pwm_level(uint32_t us, uint32_t wrap, uint32_t clk_div) {
    // Time period per tick (in us) = (clk_div / sys_clk) * 1e6
    // sys_clk = 125 MHz
    float us_per_tick = (clk_div / 125.0);
    return (uint16_t)(us / us_per_tick);
}

void print_array(uint8_t *buffer, uint8_t len){
    for (uint8_t i = 0; i < len; i++){
        if (buffer[i]& 0xF0 == 0) printf("0x%0X; ", buffer[i]);
        else printf("0x%X; ", buffer[i]);
    }
}

void scan_i2c (uint8_t *buffer, uint8_t limit){

    int read_len;
    uint8_t timeout_count           = 0;
    uint8_t generic_error_count     = 0;
    uint8_t read_address_count      = 0;
    uint8_t available_address_count = 0;
    printf("Starting scan || PICO_ERROR_GENERIC: %i || PICO_ERROR_TIMEOUT: %i\n", PICO_ERROR_GENERIC, PICO_ERROR_TIMEOUT);

    for (uint8_t addr = 0x08; addr <= 0x77; addr++) {
        // Send a dummy write — just a START + address + STOP
        read_len = i2c_read_timeout_us(I2C_PORT, addr, buffer, 2, false, 10000);
        read_address_count ++;
        switch (read_len){
            case PICO_ERROR_GENERIC:
                generic_error_count ++;
            break;
            case PICO_ERROR_TIMEOUT:
                timeout_count ++;
            break;
            default:
                available_address_count ++;
                printf("Address 0x%02X, response lenght %i; Resp: ", addr, read_len);
                print_array(buffer, 2);
                printf("\n");
            break;
        }
        sleep_ms(10); // small delay between probes
    }
    printf("Finished scan | read = %i, timeouuts = %i, generic errors = %i, available addresses = %i\n", read_address_count, timeout_count, generic_error_count, available_address_count);
}

int main()
{
    uint8_t i2c_buffer[i2c_buffer_len] = {0};
    stdio_init_all();

    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);

    // Common configuration for all servos
    const float clk_div = 64.0f;             // Slows down clock to allow 50Hz with 16-bit resolution
    const uint16_t wrap = 49999;             // 50Hz period at 64 divider: (125MHz / 64) / 50 = 39,062.5 → use 50,000 for convenience

    //Init servos
    setup_servo_pwm(SERVO1, clk_div, wrap);
    setup_servo_pwm(SERVO2, clk_div, wrap);
    setup_servo_pwm(SERVO3, clk_div, wrap);
    setup_servo_pwm(SERVO4, clk_div, wrap);
    setup_servo_pwm(SERVO5, clk_div, wrap);
    setup_servo_pwm(SERVO6, clk_div, wrap);

    // For more examples of I2C use see https://github.com/raspberrypi/pico-examples/tree/master/i2c

    scan_i2c(i2c_buffer, i2c_buffer_len);
    uint8_t ping = 0;
    set_servo_pulse(SERVO1, us_to_pwm_level(1000, wrap, clk_div)); // base(0) -> arm(5); 1
    set_servo_pulse(SERVO2, us_to_pwm_level(2000, wrap, clk_div)); // base(0) -> arm(5); 5
    set_servo_pulse(SERVO3, us_to_pwm_level(1000, wrap, clk_div)); // base(0) -> arm(5); 0
    set_servo_pulse(SERVO4, us_to_pwm_level(2000, wrap, clk_div)); // base(0) -> arm(5); 2
    set_servo_pulse(SERVO5, us_to_pwm_level(1500, wrap, clk_div)); // base(0) -> arm(5); 4
    set_servo_pulse(SERVO6, us_to_pwm_level(1000, wrap, clk_div)); // base(0) -> arm(5); 3
    while (true) {
        // Sweep from 0° to 180° (1000us to 2000us pulse)
        for (uint us = 1000; us <= 2000; us += 10) {
            uint16_t level = us_to_pwm_level(us, wrap, clk_div);
            //set_servo_pulse(SERVO1, level);
            //set_servo_pulse(SERVO2, level);
            set_servo_pulse(SERVO3, level);
            //set_servo_pulse(SERVO4, level);
            set_servo_pulse(SERVO5, level);
            set_servo_pulse(SERVO6, level);
            
            sleep_ms(50);
        }


        // Sweep back
        for (uint us = 2000; us >= 1000; us -= 10) {
            uint16_t level = us_to_pwm_level(us, wrap, clk_div);
            //set_servo_pulse(SERVO1, level);
            //set_servo_pulse(SERVO2, level);
            set_servo_pulse(SERVO3, level);
            //set_servo_pulse(SERVO4, level);
            set_servo_pulse(SERVO5, level);
            set_servo_pulse(SERVO6, level);
            sleep_ms(50);
        }
        printf("Ping | %3i;\n", ping++);
        sleep_ms(1000);
    }
}
