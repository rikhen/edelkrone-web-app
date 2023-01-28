# -----------------------------------------------------------------------------
# 
# 
# -----------------------------------------------------------------------------
import requests
import json
import time

# Local SDK endpoint URL
httpURL = "http://127.0.0.1:32222/v1"

# ---------------------------------------------------------------------------
def keyposeStoreNumeric(linkID, pan, tilt, slide, index):

  # WARNING
  # =======
  # When storing a keypose by entering specific encoder values, you must
  # specify *all* axis values for the particular bundle. If you miss even one,
  # this command returns an error.

  # ...
  url = "%s/bundle/%s" % (httpURL, linkID)
  headers = {"Content-Type": "application/json"}
  payload = {
    "command": "keyposeStoreWithNumericData",
    "index": index,
    "headPan": pan,
    "headTilt": tilt,
    "slide": slide
  }

  # ...
  response = requests.request("POST", url, headers=headers, json=payload)
  response_json = json.loads(response.text)
  print(json.dumps(response_json, indent=2))

# ---------------------------------------------------------------------------
def keyposeMoveFixedDuration(linkID, duration, index, accel):

  # WARNING
  # =======
  # With this type of fixed duration command, our motion control systems
  # can't guarantee that the motion will be completed with the given duration
  # if the given duration is shorter than what it can be achieved with %100 
  # speed.
  #
  # If the given duration is shorter than what it can be achieved with %100 
  # speed, system moves with %100 speed with the given acceleration.

  # ...
  url = "%s/bundle/%s" % (httpURL, linkID)
  headers = {"Content-Type": "application/json"}
  payload = {
    "command": "keyposeMoveFixedDuration",
    "index": index,
    "duration": duration,
    "acceleration": accel
  }

  # ...
  response = requests.request("POST", url, headers=headers, json=payload)
  response_json = json.loads(response.text)
  print(json.dumps(response_json, indent=2))

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
  print(json.dumps(response_json, indent=2))
  return response_json

# ---------------------------------------------------------------------------
if __name__ == "__main__":
  
  # ASSUMPTIONS
  # ===========
  # - HeadPLUS series product is paired with a Slider product via edelkrone
  # Web APP.
  # - linkID for the particular link Adapter copied and pasted to this
  # script after pairing is done.

  # ...
  linkID = "205C349B5853"

  # WARNING
  # =======
  # Please make sure there aren't any obstacles in the way of HeadPLUS and
  # Slider units while moving inside the motion range.

  # Full range motion limits
  panFullRange = 45.0 # in degrees
  tiltFullRange = 5.0 # in degrees
  slideFullRange = 10.0 # in centimeters

  # How many steps we want to divide the motion?
  step = 10  

  # We are using keyposeIndex=0 as a strachpad area. 
  aimIndex = 0

  # Initial positions for the motion are coming from encoder readings.
  # Therefore, the motion will start from current location group of
  # motion control systems before launching the script. So, locate your 
  # system to a *known* position before running this script.
  status = bundleStatus(linkID)
  startSlide = float(status["data"]["readings"]["slide"])
  startPan = float(status["data"]["readings"]["headPan"])
  startTilt = float(status["data"]["readings"]["headTilt"])
  keyposeStoreNumeric(linkID, startPan, startTilt, startSlide, aimIndex)

  # Small step motion duration. Please check related warning about
  # motion duration limits from the documentation.
  moveDuration_sec = 3.0
  acceleration = 0.5

  # ...
  pan = startPan
  tilt = startTilt
  slide = startSlide
    
  # For each step, how much motion will be there?
  panStep = panFullRange / step
  tiltStep = tiltFullRange / step
  slideStep = slideFullRange / step

  # ...
  for x in range(0, step):

    # ...
    print("")
    print("Motion step %d of %d ..." % (x , step))
   
    # Overwrite the keypose slot with the new setpoints at each step
    pan += panStep
    tilt += tiltStep
    slide += slideStep
    keyposeStoreNumeric(linkID, pan, tilt, slide, aimIndex)
    time.sleep(0.250)

    # Send a command to move the system to keypose location
    keyposeMoveFixedDuration(linkID, moveDuration_sec, aimIndex, acceleration)
    time.sleep(moveDuration_sec + 2.0)

  # ...
  print("Script exits.")
