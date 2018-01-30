###### App Config ######

import sys, os, app.config
INTERP = app.config.PYTHON_DIRECTORY

# INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd + app.config.APP_DIRECTORY)  # You must add your project here

from app.app import app as application

