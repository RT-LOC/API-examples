const mqtt = require('mqtt')

const mqttOptions = {
  keepalive: 50,
  clientId: `client_ ${Math.random().toString(16).substr(2, 8)}`,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 60000,
  connectTimeout: 30 * 1000,
  username: 'demo:demo@rtloc.com',
  password: '12345', // Alternative: access token instead of password
  rejectUnauthorized: false
}

// Connect to MQTT broker
const client = mqtt.connect('wss://mqtt.cloud.rtloc.com:8083/ws', mqttOptions)

// Subscribe to a few topics
client.subscribe('rtls/replay/kart/status', { qos: 0 })
client.subscribe('rtls/replay/kart/anchors', { qos: 0 })
client.subscribe('rtls/replay/kart/posxyz', { qos: 0 })

// On message: print topic and JSON message
client.on('message', (topic, message) => {
  const json = JSON.parse(message)
  console.log(`${topic} message:`)
  console.log(json)
})
