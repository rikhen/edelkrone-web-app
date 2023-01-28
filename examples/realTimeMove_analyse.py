# -----------------------------------------------------------------------------
#
#
# -----------------------------------------------------------------------------
import sys
import json
import time
import random
import requests
import datetime
import numpy as np
from scipy.special import expit
import matplotlib.pyplot as plt

# Local SDK endpoint URL
httpURL = "http://127.0.0.1:32222/v1"

# -----------------------------------------------------------------------------
def generateCurve(start, end, tick_sec, motionDuration_sec):
  sample_cnt = motionDuration_sec / tick_sec
  step = 10.0 / sample_cnt
  x = np.arange(-6, 6.0 + step, step)
  y = expit(x)
  y -= np.min(y)
  y *= (end - start) / np.max(y)
  y += start
  return y

# ---------------------------------------------------------------------------
def bundleStatus(linkID):

  # ...
  url = "%s/bundle/%s/status" % (httpURL, linkID)
  headers = {"Content-Type": "application/json"}

  # ...
  response = requests.request(
    "GET", url, headers=headers, timeout=1.0
  )
  response_json = json.loads(response.text)
  return response_json

# ---------------------------------------------------------------------------
def realTimeMoveFixedDuration(
  linkID, duration, pan, tilt, slide, focus, debug=False
):

  # WARNING
  # =======
  # When sending a real time move setpoint group, you must specify *all* real
  # time move supported axis values for the particular bundle. If you miss
  # even one, this command returns an error.

  # ...
  url = "%s/bundle/%s" % (httpURL, linkID)
  headers = {"Content-Type": "application/json"}
  payload = {
    "command": "realTimeMoveFixedDuration",
    "headPan": pan,
    "headTilt": tilt,
    "slide": slide,
    "focus": focus,
    "duration": duration
  }

  # ...
  response = requests.request("POST", url, headers=headers, json=payload)
  if (debug == True):
    response_json = json.loads(response.text)
    print(json.dumps(response_json, indent=2))

# ---------------------------------------------------------------------------
if __name__ == "__main__":

  # ASSUMPTIONS
  # ===========
  # - HeadPLUS v2 or HeadPLUS v2 PRO is paired with Slide Module v3 and
  # FocusPLUS PRO via wired setup.
  # - Pairing is completed via the edelkrone Web APP.
  # - linkID for the particular link Adapter copied and pasted to this
  # script after pairing is done.

  # ...
  linkID = "205C349B5853"

  # WARNING
  # =======
  # Please make sure there aren't any obstacles in the way of HeadPLUS,
  # Slider and Focus units while moving inside the motion range.

  # Full range motion limits
  focusMoveDelta = -15431 # encoder
  panMoveDelta = -41 # degree
  tiltMoveDelta = 4 # degree
  slideMoveDelta = 10 # centimeters

  # WARNING
  # =======
  # With this type of fixed duration command, our motion control systems
  # can't guarantee that the motion will be completed with the given duration
  # if the given duration is shorter than what it can be achieved with %100
  # speed.
  #
  # If the given duration is shorter than what it can be achieved with %100
  # speed, system moves with %100 speed with the given acceleration.

  # Total move duration for whole simulation
  totalMoveDuration_sec = 15.0

  # Step move duration for each setpoint slice
  moveDuration_sec = 0.025

  # Initial positions for the motion are coming from encoder readings.
  # Therefore, the motion will start from current location group of
  # motion control systems before launching the script. So, locate your
  # system to a *known* position before running this script.
  status = bundleStatus(linkID)
  focusStart = float(status["data"]["readings"]["focus"]) # encoder
  panStart = float(status["data"]["readings"]["headPan"]) # degrees
  tiltStart = float(status["data"]["readings"]["headTilt"]) # degrees
  slideStart  = float(status["data"]["readings"]["slide"]) # centimeters
  timestampDevice_d = int(status["data"]["timestampDevice"]) # miliseconds

  # Position curves with S-Curve approximation shape with given arguments
  fCurve = generateCurve(
    focusStart, focusStart + focusMoveDelta,
    moveDuration_sec, totalMoveDuration_sec
  )

  tCurve = generateCurve(
    tiltStart, tiltStart + tiltMoveDelta,
    moveDuration_sec, totalMoveDuration_sec
  )

  pCurve = generateCurve(
    panStart, panStart + panMoveDelta,
    moveDuration_sec, totalMoveDuration_sec
  )

  sCurve = generateCurve(
    slideStart, slideStart + slideMoveDelta,
    moveDuration_sec, totalMoveDuration_sec
  )

  # Timing variable
  tInitial = datetime.datetime.now()
  lastCommand = datetime.datetime.now()

  # ...
  tim = []
  panSetp = []
  tiltSetp = []
  focusSetp = []
  slideSetp = []
  panReading = []
  tiltReading = []
  focusReading = []
  slideReading = []

  # ...
  ind = 0
  while True:

    # Wait until another tick time
    now = datetime.datetime.now()
    if((now - lastCommand).total_seconds() >= moveDuration_sec):

      # ...
      lastCommand = now

      # Get the latest setpoints from curves
      panSetp_latest = pCurve[ind]
      tiltSetp_latest = tCurve[ind]
      slideSetp_latest = sCurve[ind]
      focusSetp_latest = fCurve[ind]

      # Get the latest readings
      status = bundleStatus(linkID)
      focusReading_latest = float(status["data"]["readings"]["focus"]) # encoder
      panReading_latest = float(status["data"]["readings"]["headPan"]) # degrees
      tiltReading_latest = float(status["data"]["readings"]["headTilt"]) # degrees
      slideReading_latest = float(status["data"]["readings"]["slide"]) # centimeters
      timestampDevice = int(status["data"]["timestampDevice"]) # miliseconds

      # Send current set of position setpoints to the bundle
      realTimeMoveFixedDuration(
        linkID, moveDuration_sec,
        panSetp_latest, tiltSetp_latest,
        slideSetp_latest, focusSetp_latest
      )

      # ...
      timestampDevice_delta = timestampDevice - timestampDevice_d

      # ...
      print("")
      print("Timestamp: %d ms (Delta: %d ms)" % (timestampDevice, timestampDevice_delta))
      print("  Pan: %.2f deg / %.2f deg" % (panReading_latest, panSetp_latest))
      print("  Tilt: %.2f deg / %.2f deg" % (tiltReading_latest, tiltSetp_latest))
      print("  Slide: %.2f cm  / %.2f cm " % (slideReading_latest, slideSetp_latest))
      print("  Focus: %.0f enc / %.0f enc" % (focusReading_latest, focusSetp_latest))

      # ...
      timestampDevice_d = timestampDevice

      # Log current setpoint / reading values
      focusSetp.append(focusSetp_latest)
      tiltSetp.append(tiltSetp_latest)
      panSetp.append(panSetp_latest)
      slideSetp.append(slideSetp_latest)
      focusReading.append(focusReading_latest)
      tiltReading.append(tiltReading_latest)
      panReading.append(panReading_latest)
      slideReading.append(slideReading_latest)
      tim.append((now - tInitial).total_seconds())

      # Finish detection
      ind += 1
      if(ind == len(fCurve)):
        break

    # ...
    time.sleep(0.001)

  # ...
  plt.figure()
  plt.subplot(2,2,1)
  plt.plot(tim, focusSetp)
  plt.plot(tim, focusReading, 'r')
  plt.subplot(2,2,2)
  plt.plot(tim, tiltSetp)
  plt.plot(tim, tiltReading, 'r')
  plt.subplot(2,2,3)
  plt.plot(tim, panSetp)
  plt.plot(tim, panReading, 'r')
  plt.subplot(2,2,4)
  plt.plot(tim, slideSetp)
  plt.plot(tim, slideReading, 'r')

  # ...
  plt.show()

  # ...
  print("Script exits.")