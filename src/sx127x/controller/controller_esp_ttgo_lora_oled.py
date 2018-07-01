from sx127x.controller import esp_controller, display_ssd1306_i2c

class TTGOController(esp_controller.ESP32Controller):

    # LoRa config
    LORA_RESET = 14

    LORA_CS = 18
    LORA_SCK = 5
    LORA_MOSI = 27
    LORA_MISO = 19

    LORA_DIO0 = 26
    LORA_DIO1 = None
    LORA_DIO2 = None
    LORA_DIO3 = None
    LORA_DIO4 = None
    LORA_DIO5 = None


    # OLED config
    OLED_RESET = 16
    OLED_SDA = 4
    OLED_SCL = 15
    OLED_I2C_ADDR = 0x3C
    OLED_I2C_FREQ = 400000
    OLED_WIDTH = 128
    OLED_HEIGHT = 32


    # ESP config
    ON_BOARD_LED_PIN_NO = 25
    ON_BOARD_LED_HIGH_IS_ON = False
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 12, 13, 14, 15, 16, 17, 18, 19, 21, 22,
                 23, 25, 26, 27, 32, 34, 35, 36, 37, 38, 39)


    def __init__(self,
                 pin_id_led = ON_BOARD_LED_PIN_NO,
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5),
                 oled_width = OLED_WIDTH,
                 oled_height = OLED_HEIGHT,
                 scl_pin_id = OLED_SCL,
                 sda_pin_id = OLED_SDA,
                 freq = OLED_I2C_FREQ):

        super().__init__(pin_id_led = pin_id_led,
                         on_board_led_high_is_on = on_board_led_high_is_on,
                         pin_id_reset = pin_id_reset,
                         blink_on_start = blink_on_start)

        self.reset_pin(self.prepare_pin(self.OLED_RESET))
        self.display = display_ssd1306_i2c.Display(
            width = oled_width,
            height = oled_height,
            scl_pin_id = scl_pin_id,
            sda_pin_id = sda_pin_id,
            freq = freq)

        self.display.show_text('Hello !')


    def add_transceiver(self,
                        transceiver,
                        pin_id_ss = LORA_CS,
                        pin_id_RxDone = LORA_DIO0,
                        pin_id_RxTimeout = LORA_DIO1,
                        pin_id_ValidHeader = LORA_DIO2,
                        pin_id_CadDone = LORA_DIO3,
                        pin_id_CadDetected = LORA_DIO4,
                        pin_id_PayloadCrcError = LORA_DIO5):

        transceiver.show_text = self.display.show_text
        transceiver.show_packet = self.show_packet

        return super().add_transceiver(transceiver,
                                       pin_id_ss,
                                       pin_id_RxDone,
                                       pin_id_RxTimeout,
                                       pin_id_ValidHeader,
                                       pin_id_CadDone,
                                       pin_id_CadDetected,
                                       pin_id_PayloadCrcError)


    def show_packet(self, payload_string, rssi = None):
        self.display.clear()
        line_idx = 0
        if rssi:
            self.display.show_text(
                'RSSI: {}'.format(rssi), x = 0, y = line_idx * 10,
                clear_first = False, show_now = False)
            line_idx += 1

        self.display.show_text_wrap(
            payload_string, start_line = line_idx, clear_first = False)

