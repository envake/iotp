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

#--------------------------------------------------------------------------

#mqtt importieren
#...

def is_reset(data):
    if ('message' in data):
        return (data['message'].payload == "Master: Actor-1 reset.")
    # N.B. not checking if 'message' is in data could lead to Exception
    # on PUBLISH packets for messages with qos equal to 2
    return False

def reset(data):
	#wenn resetet
	...
	my_client.publish(iot/Actor-1/status, "Actor-1 is reset.")

my_client = mqtt.Client("actor-1",True)
for retry in range(10):
    try:
        my_client.connect("test.mosquitto.org", 60)
        break
    except Exception as e:
        print("connecting...")
my_client.subscribe([["iot/master"]])
my_client.on(mqtt.PUBLISH, reset, is_reset)

#wenn aktor ein
#...
	my_client.publish(iot/Actor-1/status, "Actor-1 is on.")

#wenn aktor aus
#...
	my_client.publish(iot/Actor-1/status, "Actor-1 is off.")

#wenn ready
#...
	my_client.publish(iot/Actor-1/status, "Actor-1 is ready.")

my_client.loop()

#