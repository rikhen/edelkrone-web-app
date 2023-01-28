# -----------------------------------------------------------------------------
# 
# 
# -----------------------------------------------------------------------------
import cv2
import json
import time
import urllib
import requests
import numpy as np

# Local SDK endpoint URL
httpURL = "http://127.0.0.1"

# ---------------------------------------------------------------------------
def visionDiscovery():

  # ...
  url = "%s:32225/v1/vision" % (httpURL)
  headers = {"Content-Type": "application/json"}
  payload = {"command" : "visionStatus"}

  # ...
  response = requests.request(
    "POST", url, headers=headers, json=payload, timeout=1.0
  )
  response_json = json.loads(response.text)
  return response_json

# ---------------------------------------------------------------------------
if __name__ == "__main__":
  
  # ...
  visionDiscovery_json = visionDiscovery()

  # ...
  print("")
  print("Current Vision Module List")
  print("==========================")
  print(json.dumps(visionDiscovery_json, indent=2))

  # ...
  vision_linkID = visionDiscovery_json["data"][0]["linkID"]
  vision_mjpegLink = "%s:32225/%s" % (httpURL, vision_linkID)
  stream = urllib.request.urlopen(vision_mjpegLink)

  # ...
  print("")
  print("You can open following URL from your browser to watch the stream: %s" %
    vision_mjpegLink
  )

  # ...
  imdat = b''
  while True:
    imdat += stream.read(1024)
    a = imdat.find(b'\xff\xd8')
    b = imdat.find(b'\xff\xd9')
    if((a != -1) and (b != -1)):
      jpg = imdat[a:b+2]
      imdat = imdat[b+2:]
      frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
      cv2.imshow("Vision Module Stream", frame)
      if((cv2.waitKey(1) & 0xFF) == ord("q")):
        break

  # ...
  print("")
  print("Script exits.")
