# basic imports
import mcu
import streams

# Ethereum modules
from blockchain.ethereum import ethereum
from blockchain.ethereum import rpc

# WiFi drivers
from espressif.esp32net import esp32wifi as net_driver # for ESP-32
# from broadcom.bcm43362 import bcm43362 as net_driver # for Particle Photon
from wireless import wifi

# SSL module for https
import ssl

# Configuration file
import config

# mqtt library
from mqtt import mqtt

# The SSL context is needed to validate https certificates
SSL_CTX = ssl.create_ssl_context(
    cacert=config.CA_CERT,
    options=ssl.CERT_REQUIRED|ssl.SERVER_AUTH
)

try:
    streams.serial()

    # Connect to WiFi network
    net_driver.auto_init()
    print("Connecting to wifi")
    wifi.link(config.WIFI_SSID, wifi.WIFI_WPA2, config.WIFI_PASSWORD)
    print("Connected!")
    print("Asking ethereum...")

    # Init the RPC node
    eth = rpc.RPC(config.RPC_URL, ssl_ctx=SSL_CTX)

	# Init smart contract object
    led_contract = ethereum.Contract(
        eth,
        config.CONTRACT_ADDRESS,
        config.PRIVATE_KEY,
        config.ADDRESS,
        chain=ethereum.ROPSTEN
    )
    for name in config.CONTRACT_METHODS:
        method = config.CONTRACT_METHODS[name]
        led_contract.register_function(
            name,
            config.GAS_PRICE,
            method["gas_limit"],
            args_type=method["args"]
        )
except Exception as e:
print(e)


# Funktion zum prüfen, ob reset Nachricht gesendet wurde
def is_reset(data):
    if ('message' in data):
        return (data['message'].payload == "Master: Actor-1 reset.")
    return False

# Funktion zum ausführen eines resets und senden der Quittung
def reset(data):
	mcu.reset()
	my_client.publish(iot/Actor-1/status, "Actor-1 is reset.")

try:
	# mqtt setup 
	my_client = mqtt.Client("actor-1",True)
	for retry in range(10):
	    try:
	        my_client.connect(config.MQTT_BROKER_IP_ADDRESS, 60)
	        break
	    except Exception as e:
	        print("connecting...")
	# mqtt subscribtion + für reset
	my_client.subscribe([["iot/master"]])
	my_client.on(mqtt.PUBLISH, reset, is_reset)

	# Bereitschaft signalisieren
	my_client.publish(iot/Actor-1/status, "Actor-1 is ready.")

	my_client.loop()

	while True:
		sleep(4000)
		# Aufruf der readLed Funktion des Smart Contracts
		ledStatus = led_contract.call("readLed")
		#prüfen ob led eingeschaltet werden muss
		if (ledStatus == 1):
			digitalWrite(D13, 1) #?
			my_client.publish(iot/Actor-1/status, "Actor-1 is on.")
		else:
			digitalWrite(D13, 0) #?
			my_client.publish(iot/Actor-1/status, "Actor-1 is off.")
except Exception as e:
    print(e)
