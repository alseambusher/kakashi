#include <LedControl.h>
#include "ports.h"

namespace kakashi::led
{
    LedControl display = LedControl(LED_DIN, LED_CLK, LED_CS, 0);

    // https://xantorohara.github.io/led-matrix-editor
    const uint64_t SHARINGAN[] = {
        0xff3cbde7e7ffe7ef,
        0xbf9fffe5e4ff9fbf,
        0xf7e7ffe7e7bd3cff,
        0xfdf9ff27a7fff9fd,

        0x3c7effe7e7ff7e3c,
        0x3c7effe7e7ff7e3c,
        0x3c7ee7c3c3e77e3c,
        0x3c66c38181c3663c,
        
        0x3c7ebfe7e7bf7a3c, 0x3c5affe7e7bf7e3c, 0x3c5efde7e7fd7e3c, 0x3c7efde7e7ff5a3c
        };

    void displayImage(uint64_t image)
    {
        for (int i = 0; i < 8; i++)
        {
            byte row = (image >> i * 8) & 0xFF;
            for (int j = 0; j < 8; j++)
            {
                display.setLed(0, i, j, bitRead(row, j));
            }
        }
    }

    void init()
    {
        display.clearDisplay(0);
        display.shutdown(0, false);
        display.setIntensity(0, 2);
    }
};
