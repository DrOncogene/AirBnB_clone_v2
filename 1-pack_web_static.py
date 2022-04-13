#!/usr/bin/python3
from fabric.operations import local
from datetime import datetime
from fabric.decorators import task


@task
def do_pack():
    '''compresses web_static into an archive'''
    local('mkdir -p versions/')
    now = datetime.now()
    local('tar -czvf versions/web_static_{}{}{}{}{}{}.tgz web_static'.format(
            now.year, now.month, now.day, now.hour, now.minute, now.second))
