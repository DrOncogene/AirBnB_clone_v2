#!/usr/bin/python3
"""compresses the web_static folder"""
import os
from datetime import datetime
from fabric.decorators import task
from fabric.api import local


@task
def do_pack():
    '''compresses web_static into an archive'''
    if not os.path.isdir('versions'):
        os.mkdir("versions")
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )
    archive_path = "versions/{}".format(archive_name)
    try:
        local('tar -czvf {} web_static'.format(archive_path))
        print("web_static packed: {} -> {} Bytes".format(
              archive_path, os.stat(archive_path).st_size))
        return archive_path
    except Exception:
        return None
