// import { EventEmitter } from "events";
// const EventEmitter = require("events")

// export default class WsClient extends EventEmitter {
class WsClient {
  constructor(host, port, type) {

    this.server = {
      host,
      port,
      type
    };

    this.settings = {
      reconnect: true,
      retry: 3000,
      decode: true
      // data: 'all'
    };

    this.connect()
  }
  connect() {
    console.log(
      "Initiating connection to " +
        this.server.host +
        " " +
        this.server.port
    );

    this.connection = new WebSocket(
      this.server.type +
        "://" +
        this.server.host +
        ":" +
        this.server.port
    );

    this.connection.addEventListener("open", this);

    this.connection.addEventListener("close", this);

    this.connection.addEventListener("message", this);
  }
  handleEvent(evt) {
    switch (evt.type) {
      case "message":
        console.log('MSG:')
        this.decode(evt.data)
        break;
      case "open":
        this.state = WebSocket.OPEN;
        // this.emit("open");
        console.log("Connection established");
        break;
      case "close":
        console.log("Connection closed");
        this.connection.removeEventListener("open", this);
        this.connection.removeEventListener("close", this);
        this.connection.removeEventListener("message", this);

        // this.emit("close");
        break;
      default:
        console.log("Unhandled evt");
    }
  }

  decode(data) { 
    let parsed
    if (data.substr(0, 3) == "cx|") {
      parsed = JSON.parse(data.slice(10));
    } else if (data.charAt(0) === "{") {
      parsed = JSON.parse(data);
    } else {
      console.log('Received: ' + data)
    }

    if ('frames' in parsed) {
      console.log('POSXYZ');
    } else if ('anchorList' in parsed) {
      console.log('ALIST')
    } else if ('tagList' in parsed) {
      console.log('TLIST')
    }
    else if ('tagStatus' in parsed) {
      console.log('Status')
    } else {
      console.log('UNKNOWN PKT')
    }
    console.log(parsed)
  }

}

// module.exports = WsClient