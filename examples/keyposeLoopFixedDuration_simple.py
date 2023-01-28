# -----------------------------------------------------------------------------
# 
# 
# -----------------------------------------------------------------------------
import requests
import json
import time

# Local SDK endpoint URL
httpURL = "http://127.0.0.1:32222/v1"

# -----------------------------------------------------------------------------
def keyposeLoopFixedDuration(linkID, index1, index2, moveDuration_sec, acceleration):

  url = "%s/bundle/%s" % (httpURL, linkID)

  payload = {
    "command": "keyposeLoopFixedDuration",
    "index1": index1,
    "index2": index2,
    "duration": moveDuration_sec,
    "acceleration": acceleration
  }
 
  headers = {'Content-Type': 'application/json'}
  response = requests.request("POST", url, headers=headers, json=payload)
  response_json = json.loads(response.text)
  print(json.dumps(response_json, indent=2))

# ---------------------------------------------------------------------------
if __name__ == "__main__":

  # ASSUMPTIONS
  # ===========
  # - HeadPLUS series product is paired with a Slider product via edelkrone
  # Web APP.
  # - linkID for the particular link Adapter copied and pasted to this
  # script after pairing is done.
  # - Relevant keypose slots are filled beforehand via edelkrone Web APP.

  # ...
  linkID = "205C349B5853"

  # MOTION PARAMETERS
  # =================
  # NOTE: POSE1 in the edelkrone Web APP is the same as keyposeIndex=0 in
  # the SDK command since edelkrone SDK uses zero based indexing scheme.
  index1 = 0
  index2 = 2
  acceleration = 0.25
  moveDuration_sec = 10.0

  # CAUTION
  # =======
  # With this type of fixed duration command, our motion control systems
  # can't guarantee that the motion will be completed with the given duration
  # if the given duration is shorter than what it can be achieved with %100 
  # speed.
  #
  # If the given duration is shorter than what it can be achieved with %100 
  # speed, system moves with %100 speed with the given acceleration.

  # ...
  keyposeLoopFixedDuration(linkID, index1, index2, moveDuration_sec, acceleration)
  
  # ...
  print("Script exits.")
