import paho.mqtt.client as mqtt

class MqttController:
    topic_pub_available = "smartmirror/available"

    def __init__(self, mqtt_config, on_message, client_id="Guest", topics_sub=["#"]):
        self.topics_sub = topics_sub
        self.client = mqtt.Client(client_id=client_id, clean_session=False, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_message = on_message
        self.client.will_set(self.topic_pub_available, "offline", qos=1, retain=True)
        self.client.username_pw_set(username=mqtt_config.mqtt_user, password=mqtt_config.mqtt_pass)
        self.client.connect(mqtt_config.broker_address)
        self.subscribe_to_topics()
        print("Mqtt client created.")
        self.client.publish(self.topic_pub_available, "online", qos=1, retain=True)
        self.client.loop_start()

    def subscribe_to_topics(self):
        for topic in self.topics_sub:
            self.client.subscribe(topic)

    def send_message(self, topic, message):
        print("Sending:", topic, message)
        result, _ = self.client.publish(topic, message, qos=1, retain=False)
        if result != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to send message. Result code: {result}")

class MqttConfig:
    broker_address = None
    mqtt_user = None
    mqtt_pass = None

    def __init__(self, broker_address=None, mqtt_user=None, mqtt_pass=None):
        self.broker_address = broker_address
        self.mqtt_user = mqtt_user
        self.mqtt_pass = mqtt_pass

    @classmethod
    def from_json(cls, config_data):
        mqtt_config = MqttConfig(
            broker_address=config_data['mqtt']['broker_address'],
            mqtt_user=config_data['mqtt']['mqtt_user'],
            mqtt_pass=config_data['mqtt']['mqtt_pass']
        )
        return mqtt_config