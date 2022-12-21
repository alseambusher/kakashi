
#include <ArduinoLog.h>
#include "src/led.h"
#include "src/pan_and_tilt.h"

PanAndTilt pnts[2];

void setup()
{
    pnts[0].setup(PNT_1, PNT_2);
    pnts[1].setup(PNT_3, PNT_4);

    Serial.begin(9600);

    Log.begin(LOG_LEVEL_VERBOSE, &Serial);

    Serial.begin(115200);
    Serial.setTimeout(1000);

    kakashi::led::init();
}

int split(String str, String *strs, char delimiter = ' ')
{
    int count = 0;
    while (str.length() > 0)
    {
        int index = str.indexOf(delimiter);
        if (index == -1)
        {
            strs[count++] = str;
            break;
        }
        else
        {
            String out = str.substring(0, index);
            out.replace("\n", "");
            strs[count++] = out;
            str = str.substring(index + 1);
        }
    }
    return count;
}

void loop()
{
    while (!Serial.available())
        ;
    
    auto message = Serial.readStringUntil('#');
    String parsed[3];
    auto count = split(message, parsed);
    Log.notice("comms : %s %d" CR, message.c_str(), count);

    if (count == 3)
    {
        if (parsed[0] == "pan")
        {

            pnts[parsed[1].toInt()].pan(parsed[2].toInt());
        }
        if (parsed[0] == "tilt")
        {
            pnts[parsed[1].toInt()].tilt(parsed[2].toInt());
        }
    } else if (count == 2)
    {
        if (parsed[0] == "led") {
           kakashi::led::displayImage(kakashi::led::SHARINGAN[parsed[1].toInt()]);
        }
    }
    
}
