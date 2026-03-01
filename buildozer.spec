[app]
title = myPieIDE
package.name = mypie
package.domain = org.annapreston
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# CRITICAL: Include these requirements
requirements = python3,kivy,jedi,parso,pygments 
orientation = portrait 
android.arch = arm64-v8a 
android.permissions = INTERNET, CAMERA, VIBRATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, RECORD_AUDIO, 
ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, MODIFY_AUDIO_SETTINGS, 
ACCESS_BACKGROUD_LOCATION, ACCESS_HIDDEN_PROFILES, ACCESS_LOCAL_NETWORK, ACCESS_NETWORK_STATE, 
ACCESS_WIFI_STATE
