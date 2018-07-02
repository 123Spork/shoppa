def epoch(self):
    return self.datetime_to_ms_epoch(self._dt)

def ms_epoch():
    return int(time.time() * 1000)