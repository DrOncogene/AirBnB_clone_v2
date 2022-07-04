#!/usr/bin/python3
"""compresses and deploy"""
from sys import argv
from os import path as ospath
from datetime import datetime
from fabric.decorators import task, runs_once
from fabric.api import local, run, put, env, sudo


env.hosts, env.user = ['3.238.119.141', '3.234.213.52'], 'ubuntu'


@runs_once
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
    except Exception as err:
        print(err)
        return None


@task
def do_deploy(archive_path):
    """deploys web_static on to both web servers
    Args:
        archive_path(str): path to the static file archive

    Return:
        True if all ops succeeded or False
    """
    if not ospath.exists(archive_path):
        return False
    archive_name = archive_path.split('/')[-1]
    release_dir = archive_name.split('.')[0]
    try:
        put(archive_path, '/tmp/')
        sudo("mkdir -p /data/web_static/releases/{}".format(
             archive_name.split('.')[0]))
        sudo('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            archive_name, release_dir))
        sudo('rm /tmp/{}'.format(archive_name))
        sudo('mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/'.format(release_dir, release_dir))
        sudo('rm -rf /data/web_static/releases/{}/web_static'.format(
             release_dir))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s -f /data/web_static/releases/{}/\
            /data/web_static/current'.format(release_dir))
        print("New version deployed!")
        return True
    except Exception as err:
        print(err)
        return False
