const mqtt = require('mqtt')

mqttOptions = {
    keepalive: 50,
    clientId: 'client_' + Math.random().toString(16).substr(2, 8),
    protocolId: 'MQTT',
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 10000,
    connectTimeout: 30 * 1000,
    username: '',
    password: '',
    rejectUnauthorized: false
}

// Connect to MQTT broker
const client = mqtt.connect('mqtt://localhost:1883', mqttOptions)

// Subscribe to a few topics
client.subscribe('data/#', { qos: 0 })

// On message: print topic and JSON message
client.on('message', function(topic, message) {
    const json = JSON.parse(message)
    console.log(topic + ' message:')
    console.log(json)
})