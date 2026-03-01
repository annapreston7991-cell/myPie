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
permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.arch = arm64-v8a

