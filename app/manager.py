# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load and save your docker-volumes."""

import click
import datetime
import os
import utils
from future.utils import raise_with_traceback as rwt


@click.group()
def cli():
    """Showcase different options to backup and load docker volumes."""
    pass


@cli.command()
@click.option('--volume', required=True, type=click.STRING, help='The named volume to save locally. ')
@click.option('--path',  default='./', type=click.Path(exists=True, file_okay=False, resolve_path=True, writable=True),
              help='The path to save the docker volume as .tar.gz')
@click.option('--interactive', default='True', type=click.BOOL, help='Run the script interactively')
def save(volume, path, interactive):
    """Save your docker volume locally."""
    exporting_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    filename = volume + "_" + exporting_time + ".tar.gz"
    save_cmd = "docker run --rm --volume {0}:/mybackup -v {1}:/backup ubuntu tar czvf /backup/{2} /mybackup".format(
        volume, path, filename)

    if utils.docker_volume_exist(volume):
        if interactive:
            if click.confirm('Do you want to continue', abort=True):
                utils.execute_subprocess(save_cmd)
        else:
            utils.execute_subprocess(save_cmd)
        utils.echo(msg='\nSuccessfully exported docker volume at: {0}\n'.format(
            os.path.join(path, filename)), color='green')
    else:
        msg = "docker volume '{}' does not exist. ".format(volume)
        utils.echo(msg, 'red')


@cli.command()
@click.option('--volume', required=True, type=click.STRING, help='The named volume where the zip is to be uploaded. ')
@click.option('--path',  required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True),
              help='The path to load the zip or tar or tar.gz from.')
@click.option('--interactive', default='True', type=click.BOOL, help='Run the script interactively')
def load(volume, path, interactive):
    """Load the locally saved volume to named docker-volume."""
    path, filename = utils.get_filename_from_path(path)
    allowed, extension = utils.allowed_files(filename)
    if not allowed:
        rwt('File extension not allowed', traceback=Ellipsis)
    load_cmd = 'docker run --rm --volume {0}:/mybackup -v {1}:/backup ubuntu bash -c "cd /mybackup && tar xvf /backup/{2} --strip 1"'.format(
        volume, path, filename)
    if utils.docker_volume_exist(volume) and click.confirm(utils.echo('The named volume already exists.\nDo you wish to overwrite?', 'red'), abort=True):
        utils.execute_subprocess(load_cmd)
    else:
        if interactive and click.confirm('Safe to upload the named volume. Do you want to continue', abort=True):
            utils.execute_subprocess(load_cmd)
        else:
            utils.execute_subprocess(load_cmd)

    utils.echo(msg='\nSuccessfully imported docker volume at: {0} as {1}\n'.format(
        os.path.join(path, filename), volume), color='green')
