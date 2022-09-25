import traceback


class QueueRunner():

  def run(self):
    while True:
      item = self.queue.get()
      try:
        item['f'](*item['a'])
      except:
        traceback.print_exc()

