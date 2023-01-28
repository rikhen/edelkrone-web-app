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
if __name__ == "__main__":
  
  # ASSUMPTIONS
  # ===========
  # - Pairing is completed via the edelkrone Web APP
  # - linkID for the particular link Adapter copied and pasted to this
  # script after pairing is done.

  # ...
  linkID = "205C349B5853"

  # ...
  for x in range(0, 10):

    # ...
    print("")
    print("Status query %d of %d ..." % (x , 10))
   
    # ...
    status = bundleStatus(linkID)
    print(json.dumps(status, indent=2))

    # ...
    time.sleep(0.25)

  # ...
  print("Script exits.")
