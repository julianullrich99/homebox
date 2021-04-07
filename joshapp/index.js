<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, minimal-ui, viewport-fit=cover">
  <link rel="stylesheet" href="css/style.css">
  <title>Homecontrol</title>
</head>

<body>
<div class="header">
<div  id="reddingclock">18:29</div>
<div id="melauneclock">12:29</div>

</div>

<section id="main">



  <!-- <div class="preferncebox">
  <div class="roomname">Clock
    </div>
    <div class="prefernce">
      <div  id="reddingclock">18:29</div>
      <div id="melauneclock">12:29</div>
      </div>
  </div> -->

<div class="preferncebox">
<div class="roomname">Kitchen
  </div>
  <div class="prefernce">
<input type="range" min="0" max="100" id="kitchen" class="range vertical-highest-first round">
    </div>
</div> 
<div class="preferncebox">
<div class="roomname">Livingroom
  </div>
  <div class="prefernce Livingroom">
<div class="colorpicker" id="LivingroomColor"></div>
    </div>
</div>
<!-- <div class="preferncebox">
<div class="roomname">Timer
  </div>
  <div class="prefernce Timer">
    <div  id="reddingclock">18:29</div>
    <div id="melauneclock">12:29</div>
</div> -->
</section>

  <script src="dist/iro.js"></script>
  <script src="dist/script.js"></script>
</body>

</html>
