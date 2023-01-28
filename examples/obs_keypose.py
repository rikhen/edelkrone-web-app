# ------------------------------------------------------------
# 
#
# ------------------------------------------------------------
import obspython as obs
import json
import requests
import time

# ------------------------------------------------------------
url = "http://127.0.0.1:32222/v1/bundle/"
link_id = int(0)

# ------------------------------------------------------------
def update_keypose(index):

  payload = json.dumps({
    "command": "keyposeMoveFixedSpeed",
    "index": index,
    "speed": 0.75, # Relative speed
    "acceleration": 0.5 # Relative acceleration
  })
  
  headers = {
    'Content-Type': 'application/json'
  }
  
  response = requests.request(
    "POST", url, headers=headers, data=payload
  )

# ------------------------------------------------------------
def wait_for_motion():
  global url
  data = {}
  for i in range(0,1000):
    status_url = url + "/status"
    payload = {}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", status_url, headers=headers, json=payload)
    data = response.json()
    print(data["data"]["state"])
    if data["data"]["state"] == "idle":
      time.sleep(0.5)
      return 

# ------------------------------------------------------------
def on_event(event):
  
  # ...
  if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
  
    # ...
    source = obs.obs_frontend_get_current_scene()
    scene_name = obs.obs_source_get_name(source)
    
    # Fill your scene name
    if (scene_name == "Scene 1"):
      update_keypose(0)
    
    # ...
    if (scene_name == "Scene 2"):
      update_keypose(1)
      
      # It waits until your keypose move is finished
      wait_for_motion()
      update_keypose(2)

    # ...
    if (scene_name == "Scene 3"):
      update_keypose(2)

# ------------------------------------------------------------
def script_description():
	return "This script written by edelkrone for edelkrone SDK users. It is completely free to use or development"

# ------------------------------------------------------------
def script_update(settings):
  global link_id
  global url
  link_id = obs.obs_data_get_string(settings, "link_id")
  url = url + link_id
  obs.obs_frontend_add_event_callback(on_event)

# ------------------------------------------------------------
def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "interval", 30)

# ------------------------------------------------------------
def script_properties():
  props = obs.obs_properties_create()
  obs.obs_properties_add_text(props, "link_id", "Link ID", obs.OBS_TEXT_DEFAULT)
  return props
