import machine
import pyb
import math
from pyb import Pin
from pyb import Timer

class SM:
 def __init__(self, name, timer, pul, const, channel):
  self.n = name
  self.t = timer
  self.p = pul
  self.p.low()
  self.con = const
  self.chan = channel
  self.gzOld = 0
  self.gzNew = 0
  self.pul_width = 9000

 def iRoundPerMin(self):
  return int(self.gzOld / (self.con / 60))

 def fRoundPerMin(self):
  return float(self.gzOld / (self.con / 60))

 def getRoundPerMin(self, rpm):
  gzNew = int(rpm * (self.con / 60))
  while rpm > (gzNew / (self.con / 60)):
   gzNew = gzNew + 1
  return gzNew

 def setRoundPerMin(self, rpm):
  self.gzNew = int(rpm * (self.con / 60))
  while rpm > (self.gzNew / (self.con / 60)):
   self.gzNew = self.gzNew + 1

 def Accel(self):
  if self.gzOld == 0 and self.gzNew > self.gzOld:
   self.t.init(freq=1)
   ch = self.t.channel(self.chan, pyb.Timer.PWM, pin=self.p, pulse_width=self.pul_width)
  if self.gzNew > self.gzOld:
   dif = math.sqrt(self.gzNew - self.gzOld) // 1
   self.gzOld = self.gzOld + int(dif)
   self.t.freq(self.gzOld)
  else: 
   self.gzOld = self.gzNew
   if self.gzOld == 0:
    self.t.deinit()
   else:
    self.t.freq(self.gzOld)

 def Stop(self):
  self.gzOld == 0
  self.t.deinit()
