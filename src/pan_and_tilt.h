#include <Servo.h>

class PanAndTilt {
public:
    void setup(int port_pan, int port_tilt) {
        m_pan_servo.write(0);
        m_tilt_servo.write(0);
        m_pan_servo.attach(port_pan);
        m_tilt_servo.attach(port_tilt);
    }

    void pan(int value) {
       m_pan_servo.write(value);
    }

    void tilt(int value) {
       m_tilt_servo.write(value);
    }
private:
    Servo m_pan_servo, m_tilt_servo;
};