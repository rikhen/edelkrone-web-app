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
def shutterTrigger(linkID, triggerDuration_ms):

  url = "%s/bundle/%s" % (httpURL, linkID)

  payload = {
    "command": "shutterTrigger",
    "triggerDuration_ms": triggerDuration_ms
  }

  headers = {'Content-Type': 'application/json'}
  response = requests.request("POST", url, headers=headers, json=payload)
  response_json = json.loads(response.text)
  print(json.dumps(response_json, indent=2))

# ---------------------------------------------------------------------------
if __name__ == "__main__":

  # ASSUMPTIONS
  # ===========
  # - Edelkrone product is paired via edelkrone Web APP.
  # - linkID for the particular link Adapter copied and pasted to this
  # script after pairing is done.
  # - Relevant keypose slots are filled beforehand via edelkrone Web APP.

  # ...
  linkID = "2060344D5530"

  # SHUTTER TRIGGER PARAMETERS
  # ==========================
  # Shutter trigger duration in milliseconds
  triggerDuration_ms = 250

  # ...
  shutterTrigger(linkID, triggerDuration_ms)

  # ...
  print("Script exits.")
