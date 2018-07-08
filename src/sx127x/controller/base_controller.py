from time import sleep


class BaseController:

    ON_BOARD_LED_PIN_NO = None
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = []
                 
    LORA_RESET = None
    
    LORA_CS = None
    LORA_SCK = None
    LORA_MOSI = None
    LORA_MISO = None
                    
    LORA_DIO0 = None
    LORA_DIO1 = None
    LORA_DIO2 = None
    LORA_DIO3 = None
    LORA_DIO4 = None
    LORA_DIO5 = None
     
    
    def __init__(self,
                 pin_id_led = ON_BOARD_LED_PIN_NO, 
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5)):                 

        self.pin_led = self.prepare_pin(pin_id_led)
        self.on_board_led_high_is_on = on_board_led_high_is_on
        self.pin_reset = self.prepare_pin(pin_id_reset)        
        self.reset_pin(self.pin_reset)
        self.spi = self.prepare_spi(self.get_spi())        
        self.transceivers = {}
        self.blink_led(*blink_on_start) 
        

    def add_transceiver(self, 
                        transceiver, 
                        pin_id_ss = LORA_CS,
                        pin_id_RxDone = LORA_DIO0,
                        pin_id_RxTimeout = LORA_DIO1,
                        pin_id_ValidHeader = LORA_DIO2,
                        pin_id_CadDone = LORA_DIO3,
                        pin_id_CadDetected = LORA_DIO4,
                        pin_id_PayloadCrcError = LORA_DIO5):
        
        transceiver.blink_led = self.blink_led
        transceiver.pin_ss = self.prepare_pin(pin_id_ss)
        transceiver.pin_RxDone = self.prepare_irq_pin(pin_id_RxDone)
        transceiver.pin_RxTimeout = self.prepare_irq_pin(pin_id_RxTimeout)
        transceiver.pin_ValidHeader = self.prepare_irq_pin(pin_id_ValidHeader)
        transceiver.pin_CadDone = self.prepare_irq_pin(pin_id_CadDone)
        transceiver.pin_CadDetected = self.prepare_irq_pin(pin_id_CadDetected)
        transceiver.pin_PayloadCrcError = self.prepare_irq_pin(pin_id_PayloadCrcError)
        
        transceiver.init()        
        self.transceivers[transceiver.name] = transceiver 
        return transceiver
        
                 
    def prepare_pin(self, pin_id, in_out = None):
        reason = '''
            # a pin should provide:
            # .pin_id
            # .low()
            # .high()
            # .value()  # read input.
            # .irq()    # (ESP8266/ESP32 only) ref to the irq function of real pin object.
        '''
        raise NotImplementedError('reason')
        

    def prepare_irq_pin(self, pin_id):
        reason = '''
            # a irq_pin should provide:
            # .set_handler_for_irq_on_rising_edge()  # to set trigger and handler.
            # .detach_irq()
        '''
        raise NotImplementedError('reason')
        
        
    def get_spi(self): 
        reason = '''
            # initialize SPI interface 
        '''
        raise NotImplementedError('reason')  
        
        
    def prepare_spi(self, spi): 
        reason = '''
            # a spi should provide: 
            # .close()
            # .transfer(pin_ss, address, value = 0x00) 
        '''
        raise NotImplementedError('reason')        


    def led_on(self, on = True):
        self.pin_led.value(1) if self.on_board_led_high_is_on == on else self.pin_led.value(0)
            

    def blink_led(self, times = 1, on_seconds = 0.1, off_seconds = 0.1):
        for i in range(times):
            self.led_on(True)
            sleep(on_seconds)
            self.led_on(False)
            sleep(off_seconds) 
            

    def reset_pin(self, pin, duration_low = 0.05, duration_high = 0.05):
        pin.value(0)
        sleep(duration_low)
        pin.value(1)
        sleep(duration_high)
        
        
    def __exit__(self): 
        self.spi.deinit()