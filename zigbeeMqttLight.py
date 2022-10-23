from zigbeeMqtt import zigbeeMqtt


class zigbeeMqttLight(zigbeeMqtt):
  def __init__(self, config=..., name=""):
    super().__init__(config, name)

    self.state = False
    self.brightness = 254
    self.colorTemp = 254

  def set(self, key, value):
    if key == 'toggle':
      self.state = not self.state

      if self.state:
        self.turnOn()
      else:
        self.turnOff()
    
    elif key == 'state':
      self.state = not (value == 'ON') # not here because we're toggling anyway
      self.toggle()
      
    elif key == 'brightness':
      if value == '0':
        self.turnOff()
      else:
        self.brightness = int(value)
        self.turnOn()

    else:
      super().set(key, value)

    if (key == 'color_temp'): self.colorTemp = int(value)
    
  def turnOn(self):
    self.state = True
    super().set('brightness', self.brightness)
    super().set('color_temp', self.colorTemp)

  def turnOff(self):
    self.state = False
    super().set('state', 'OFF')
  
  def okay(self):
    self.queue.put({ 'f':self.set, 'a':['effect', 'okay'] })
  
  def toggle(self, brightness = None, colorTemp = None, reset = False):
    if brightness is not None:
      self.brightness = brightness
      self.state = False # treat as if its off -> switch on in any case
    if colorTemp is not None:
      self.colorTemp = colorTemp
      self.state = False # treat as if its off -> switch on in any case
    if reset:
      self.brightness = 254
      self.colorTemp = 254
      self.state = False

    self.set('toggle', '')

