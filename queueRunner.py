import traceback


class QueueRunner():

  def run(self, nowait=False, loop=True):
    while True:
      item = None
      if (nowait): item = self.queue.get_nowait()
      else: item = self.queue.get()
      try:
        item['f'](*item['a'])
      except:
        traceback.print_exc()
      if not loop: break

