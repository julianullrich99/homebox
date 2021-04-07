// window.screen.orientation.lock('portrait');

//
// var demo = new iro.ColorPicker("#colorWheelDemo", {
//   width: window.innerWidth,
//  height: window.innerWidth,
//   markerRadius: 16,
//   color: "#f00",
//   borderWidth: 2,
//   padding: 8,
//   css: {
//     body: {
//       "background-color": "rgb",
//       "color": "rgb"
//     },
//     ".test": {
//       "border-color": "rgb",
//       "color": "rgb"
//     }
//   }
// });


function getcolorarr() {
  var bgcolor = document.getElementsByClassName('Livingroom')[0].style.borderColor;
  bgcolor = bgcolor.substring(4, bgcolor.length - 1);
  array = bgcolor.split(",");
  newarray = [];
  newarray[0] = parseInt(array[1].trim());
  newarray[1] = parseInt(array[0].trim());
  newarray[2] = parseInt(array[2].trim());
  // console.log(array);
  return newarray;
}

function postcolor(type) {
  console.log('postcolor');
  if (type == 'color') {
    var c = getcolorarr();
  } else {
    var c = [0, 0, 0];
  }

  return c;
}
window.onload = function() {

  class send {
    constructor() {
      this.link = 'http://homebox:8080/joshColor';
    }
    httpRequest(address, reqType, asyncProc) {
      var r = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
      if (asyncProc) {
        r.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            // asyncProc(this);
            console.info('success');
          }
        };
      }

      //  r.timeout = 4000;  // Reduce default 2mn-like timeout to 4 s if synchronous
      r.open(reqType, address, !(!asyncProc));
      r.send();
      return r;
    }
    livingroom(color) {
      console.log(this.httpRequest(this.link + "?r=" + parseInt(color[2]) + "&g=" + parseInt(color[0]) + "&b=" + parseInt(color[1]), "GET", true).responseText);
    }
  }



  window.publish = new send();


  function saveIP(ip) {
    window.localStorage.setItem("IP", ip);
  }

  function ajax_color(target) {
    if (target == "setleds?fade=1000" || target == "wave?fade=5000") {

      var body_styles = window.getComputedStyle(document.getElementsByTagName("body")[0]);
      var bgcolor = body_styles.backgroundColor;
      bgcolor = bgcolor.substring(4, bgcolor.length - 1);
      array = bgcolor.split(",");
      target += "&r=" + array[0] + "&g=" + array[1] + "&b=" + array[2];
    }
    if (target == "brightness") {

      target += "brightness=" + document.getElementById('brightness').value;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("demo").innerHTML = this.responseText;
      }
    };
    xhttp.open("GET", "http://" + window.localStorage.getItem("IP") + "/" + target, true);
    var link = window.localStorage.getItem("IP") + "/" + target;
    xhttp.send();
  }


  var demo = new iro.ColorPicker("#LivingroomColor", {
    // width: window.innerWidth - 40,
    // height: window.innerWidth - 40,
    width: 300,
    height: 300,
    markerRadius: 5,
    color: "#f00",
    borderWidth: 2,
    padding: 2,
    css: {
      ".wheel": {
        "background-color": "rgb",
      },
      "#colorWheelalarm": {
        "background-color": "rgb",
      },
      ".Livingroom": {
        "border-color": "rgb",
      }
    }
  }, function(callback) {
    console.log(callback);
    // colorChangeHandler();

  });

    window.currentColor = null;

  // make a handler function that will log the color's hex value to the console
  function colorChangeHandler1() {
    console.log(window.currentColor)
    var ar = [];
    var color = window.currentColor;
    ar[0] = color.rgb.g;
    ar[1] = color.rgb.b;
    ar[2] = color.rgb.r;

    window.publish.livingroom(ar);
  }

  function saveCurrentColor(color){
    window.currentColor = color;
  }

  // start listening to the color change event, now colorChangeHandler will be called whenever the color changes
  demo.on("input:end", colorChangeHandler1);
  demo.on("color:change", saveCurrentColor);

  document.getElementById('LivingroomColor').addEventListener('touchend', function() {
    window.publish.livingroom(postcolor('color'));

  }, false);

  // make a handler function that will log the color's hex value to the console
  function colorChangeHandler() {
    // console.log(color.hexString)
    // postcolor('color');

    window.publish.livingroom(postcolor('color'));

  }

}
