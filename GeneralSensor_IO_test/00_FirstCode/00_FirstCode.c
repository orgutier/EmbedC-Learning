#include <stdio.h>
#include "pico/stdlib.h"


int main (){
    const uint led_pin = 25;
    bool io_state = false;

    // Configure led pin
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    // Loop forever
    while(true){
        // Blink led
        gpio_put(led_pin, io_state);
        io_state ^= true; // Toggle
        sleep_ms(1000); // Low power function
    }
}