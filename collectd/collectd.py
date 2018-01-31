from os import listdir
from os.path import isfile, join
mypath="C:\\Projects\\monitoring_root\\monitoring\loader\\vehicle-event-router-staging-yaml-concept"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)