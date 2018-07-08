import time
from sx127x import config


msgCount = 0            # count of outgoing messages
INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
 

def duplex_callback(lora):
    print("LoRa Duplex with callback")
    lora.onReceive(on_receive)  # register the receive callback
    do_loop(lora)


def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0
    
    while True:
        now = config.millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            message = "{} {}".format(config.CONFIG.NODE_NAME, msgCount)
            send_message(lora, message)                              # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode


def send_message(lora, outgoing):
    lora.println(outgoing)
    print("Sending message:\n{}\n".format(outgoing))


def on_receive(lora, payload):
    lora.blink_led()   
    payload_string = payload.decode()
    rssi = lora.packetRssi()
    print("*** Received message ***\n{}".format(payload_string))
    if config.CONFIG.IS_TTGO_LORA_OLED:
        lora.show_packet(payload_string, rssi)
    print("with RSSI {}\n".format(rssi))
