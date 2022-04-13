#!/usr/bin/python3
import os
from datetime import datetime
from fabric.decorators import task, runs_once
from fabric.network import connect
from fabric.api import local, run, put, env


env.hosts, env.user = ['44.192.32.161', '34.139.191.175'], 'ubuntu'


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
    archive_path = f"versions/{archive_name}"
    try:
        local(f'tar -czvf {archive_path} web_static')
        print("web_static packed: {} -> {} Bytes".format(
              archive_path, os.stat(archive_path).st_size))
        return archive_path
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """deploys web_static on to both web servers
    Args:
        archive_path(str): path to the static file archive

    Return:
        True if all ops succeeded or False
    """
    if not os.path.exists(archive_path):
        return False
    archive_name = archive_path.split('/')[-1]
    release_dir = archive_name.split('.')[0]
    try:
        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}".format(
             archive_name.split('.')[0]))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            archive_name, release_dir))
        run(f'rm /tmp/{archive_name}')
        run(f'mv /data/web_static/releases/{release_dir}/web_static/*\
            /data/web_static/releases/{release_dir}/')
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
             release_dir))
        run('rm -rf /data/web_static/current')
        run(f'ln -s -f /data/web_static/releases/{release_dir}/\
             /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    """Packs web_static and deploys it to the remote servers.
    Args: None
    Return: True if all ops succeeded or False
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
