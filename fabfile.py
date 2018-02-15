# http://docs.pyinvoke.org/en/latest/getting_started.html#defining-and-running-task-functions
from fabric.api import local


def host():
    local('uname -n')

