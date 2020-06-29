load('api_config.js');
load('api_gpio.js');
load('api_mqtt.js');
load('api_sys.js');
load('api_timer.js');
load("api_pwm.js");
load('api_esp32.js');
load('api_timer.js');
load('api_uart.js');
load('api_http.js');
load('api_math.js');

//esp32_183E8C

let fontColor = 65535;

let subbed = false;

let alarmId = 0;
let pageResetTimerId = 0;

let uartBuffer = "";
let uartEnd = false;

let colorPresetsGlobal = [
  [255, 255, 255],
  [0, 0, 0],
  [127, 127, 127],
  [255, 0, 0],
  [0, 255, 0],
  [0, 0, 255],
  [255, 100, 255],
  [255, 255, 0],
  [0, 255, 255]
];

print('helloworld');

let EndCom = "\xff\xff\xff";
let uartNo = 1; // Uart number used for this example
let rxAcc = ''; // Accumulated Rx data, will be echoed back to Tx
let value = false;

UART.setConfig(uartNo, {
  baudRate: 9600,
  esp32: {
    gpio: {
      rx: 13,
      tx: 14,
    },
  },
});

function stringReplace(input, old, replace) {
  let buffer = "";
  for (let i = 0; i < input.length; i++) {
    if (input[i] === old) {
      buffer += replace;
    } else {
      buffer += input[i];
    };
  };
  return buffer;
}

function parseUart1(data) {
  // print(data.substring(1,4));
  //  print(data.slice(0,1));
  if (data.slice(0, 1) === "\xff" || data.slice(0, 1) === "\x1a") {
    parseUart1(data.slice(1));
  } else {
    return data;
  }
}

function parseUart2(data1) {
  let data = JSON.stringify(data1);
  // print(data.length);
  for (let i = 0; i < data.length; i++) {
    if (data.slice(i, i + 1) === "#") {
      uartEnd = true;
      return data.slice(0, i);
    };
  }
  return data;
}

function parseResponse(data) {
  // let dataIn = JSON.stringify(data);
  uartEnd = false;
  uartBuffer = "";
  let input = stringReplace(data, "'", '"');
  // print(test);
  print("UART: " + input);
  let arr = JSON.parse(input);
  // print(arr);
  if (arr.type === "light") {
    actionLight(arr);
  } else if (arr["type"] === "timer") {
    return;
  } else if (arr["type"] === "page") {
    startPageResetTimer(arr["value"]);
  }
}

function actionLight(arr) {
  let path = "http://192.168.178.29/redding/";
  let target = {
    "color": {
      "living": "script.php",
      "bedroom": "roomlightRGB.php"
    },
    "colorPreset": {
      "living": "script.php",
      "bedroom": "roomlightRGB.php"
    },
    "brightness": {
      "kitchen": "white.php"
    }
  };
  let payload = "";
  if (arr["action"] === "color") {
    payload = "?r=" + JSON.stringify(arr["value"][0]) + "&g=" + JSON.stringify(arr["value"][1]) + "&b=" + JSON.stringify(arr["value"][2]);
  } else if (arr["action"] === "colorPreset") {
    payload = "?r=" + JSON.stringify(colorPresetsGlobal[arr["value"]][0]) + "&g=" + JSON.stringify(colorPresetsGlobal[arr["value"]][1]) + "&b=" + JSON.stringify(colorPresetsGlobal[arr["value"]][2]);
  } else if (arr["action"] === "brightness") {
    payload = "?v=" + JSON.stringify(arr["value"]);
  };
  let url = path + target[arr["action"]][arr["target"]] + payload;
  request(url);
}

function startPageResetTimer(pagename){
  Timer.del(pageResetTimerId);
  if (pagename !== "clock"){
    pageResetTimerId = Timer.set(60000, 0, function(){
      UART.write(uartNo, 'page clock' + EndCom);
    }, null);
  };
}

UART.setDispatcher(uartNo, function(uartNo) {
  let ra = UART.readAvail(uartNo);
  if (ra > 0) {
    let data = UART.read(uartNo);
    let parsed = parseUart2(parseUart1(data));
    // print(data);
    // print(parsed);
    // print(uartBuffer);
    uartBuffer += parsed;
    if (uartEnd) {
      parseResponse(uartBuffer.slice(1));
    };
  };
}, null);

function alarm() {
  global.on = true;
  alarmId = Timer.set(1500, Timer.REPEAT, function() {
    let requestUrl1 = "http://192.168.178.29/redding/white.php?v=";
    let requestUrl2 = "http://192.168.178.29/redding/script.php?g=0&r=0&b=";
    let requestUrl3 = "http://192.168.178.29/redding/roomlight.php?color=";
    let value = !on ? "0" : "100";
    let value2 = !on ? "0" : "255";
    let value3 = !on ? "000000" : "ff0000";
    request(requestUrl1 + value);
    request(requestUrl2 + value2);
    request(requestUrl3 + value3);
    print(on);
    on = on ? false : true;
  }, null);
}

function request(requestUrl) {
  HTTP.query({
    url: requestUrl
  });
}

function switchMode(mode) {
  if (mode === 0) {
    UART.write(uartNo,
      "dims=1" + EndCom +
      "punkte.pco=25388" + EndCom +
      "thour.pco=25388" + EndCom +
      "tminute.pco=25388" + EndCom +
      // "t0.pco=25388"+EndCom+
      // "t1.pco=25388"+EndCom+
      "thome.pco=0" + EndCom +
      "tdate.pco=0" + EndCom
    );
    fontColor = 25388;
  } else {
    UART.write(uartNo,
      "dims=40" + EndCom +
      "punkte.pco=65535" + EndCom +
      "thour.pco=65535" + EndCom +
      "tminute.pco=65535" + EndCom +
      // "t0.pco=65535"+EndCom+
      // "t1.pco=65535"+EndCom+
      "thome.pco=65535" + EndCom +
      "tdate.pco=65535" + EndCom
    );
    fontColor = 65535;
  }
}
// Enable Rx
UART.setRxEnabled(uartNo, true);

MQTT.setEventHandler(function(conn, ev, edata) {
  if (ev === MQTT.EV_CONNACK && !subbed) {
    print('subbing mqtt');
    let topic = 'julian/redding/clock/test';
    MQTT.sub(topic, function(conn, topic, msg) {
      print('new value ' + topic + ' ' + msg);
      action(msg);
    });
    topic = 'julian/redding/clock/brightness';
    MQTT.sub(topic, function(conn, topic, msg) {
      print('new value ' + topic + ' ' + msg);
      UART.write(uartNo, "dims=" + msg + EndCom);
    });
    MQTT.sub('julian/redding/clock/mode', function(conn, topic, msg) {
      print('new value ' + topic + ' ' + msg);
      switchMode(JSON.parse(msg));
    });
    subbed = true;
  }
}, null);

GPIO.set_mode(2, GPIO.MODE_OUTPUT);

function action(msg) {
  GPIO.write(2, JSON.parse(msg));
  if (msg === "1") {
    alarm();
  } else {
    Timer.del(alarmId);
  };
}

let tick = true;
print(Timer.now());
Timer.set(1000, Timer.REPEAT, function() {
  let now = Timer.now() - (8 * 60 * 60);
  let timestring = Timer.fmt("%H:%M:%S", now);
  let timeHour = JSON.stringify((24 + Math.floor(now % 86400 / 3600)) % 24);
  // let timeHour = "1";
  let timeMinute = JSON.stringify(Math.floor(now % 3600 / 60));
  // let timeMinute = "0";
  let home = Timer.now() + (60 * 60);
  let homeString = Timer.fmt("%H:%M", home);
  let dateString = Timer.fmt("%A, %d.%m.%Y", now);
  // print(Timer.fmt("%w:%H:%M",now));
  // let weekdayNo = JSON.parse(Timer.fmt("%w",now);
  // dateString = weekday[weekdayNo] + ", " + dateString;
  // print(timestring);
  if (timeHour.length < 2) timeHour = "0" + timeHour;
  if (timeMinute.length < 2) timeMinute = "0" + timeMinute;
  let dots = tick ? fontColor : 0;

  if (JSON.parse(timeHour) === 6 && JSON.parse(timeMinute) === 0){
    switchMode(1);
  }
  // let dots2 = !tick ? fontColor : 0;
  MQTT.pub("julian/redding/clock/time", JSON.stringify(timestring), 1);
  UART.write(uartNo, 't0.bco=' + JSON.stringify(dots) + EndCom);
  UART.write(uartNo, 't1.bco=' + JSON.stringify(dots) + EndCom);
  UART.write(uartNo, 'thour.txt="' + timeHour + '"' + EndCom);
  UART.write(uartNo, 'tminute.txt="' + timeMinute + '"' + EndCom);
  UART.write(uartNo, 'thome.txt="' + homeString + '"' + EndCom);
  UART.write(uartNo, 'tdate.txt="' + dateString + '"' + EndCom);
  tick = tick ? false : true;
  print("tick:" + JSON.stringify(tick));
}, null);

// JamiesonCourt932
// Send UART data every second
// Timer.set(1000 /* milliseconds */, Timer.REPEAT, function() {
//   value = !value;
//   UART.write(
//     uartNo,
//     'Hello UART! '
//       + (value ? 'Tick' : 'Tock')
//       + ' uptime: ' + JSON.stringify(Sys.uptime())
//       + ' RAM: ' + JSON.stringify(Sys.free_ram())
//       + (rxAcc.length > 0 ? (' Rx: ' + rxAcc) : '')
//       + '\n'
//   );
//   rxAcc = '';
// }, null);
