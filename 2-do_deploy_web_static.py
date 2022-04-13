#!/usr/bin/python3
from os import path as ospath
from datetime import datetime
from fabric.decorators import task
from fabric.network import connect
from fabric.api import local, run, put, env


env.hosts, env.user = ['44.192.32.161', '34.139.191.175'], 'ubuntu'


@task
def do_deploy(archive_path):
    '''deploys web_static on to both web servers
    Args:
        archive_path(str): path to the static file archive

    Return:
        True if all ops succeeded or False
    '''
    if not ospath.exists(archive_path):
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
