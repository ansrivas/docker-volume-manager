# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load and save your docker-volumes."""

import os
import app
import sys
import click
import datetime
from app import utils
from future.utils import raise_with_traceback as rwt


@click.group()
@click.version_option(app.__version__)
def cli():
    """Showcase different options to backup and load docker volumes."""
    pass


@cli.command()
@click.option('--volume',
              required=True,
              type=click.STRING,
              help='The named volume to save locally. ')
@click.option('--path',
              default='./',
              type=click.Path(exists=True,
                              file_okay=False,
                              resolve_path=True,
                              writable=True),
              help='The path to save the docker volume as .tar.gz')
@click.option('--interactive',
              default='True',
              type=click.BOOL,
              help='Run the script interactively')
def save(volume, path, interactive):
    """Save your docker volume locally."""
    exporting_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    filename = volume + "_" + exporting_time + ".tar.gz"

    save_cmd = utils.save_cmd.format(volume, path, filename)

    if not utils.docker_volume_exist(volume):
        msg = "docker volume '{}' does not exist. ".format(volume)
        utils.echo(msg, 'red')
        sys.exit(1)

    if interactive:
        click.confirm('Do you want to continue', abort=True)

    utils.execute_subprocess(save_cmd)
    utils.echo(msg='\nSuccessfully exported docker volume at: {0}\n'.format(
        os.path.join(path, filename)), color='green')


@cli.command()
@click.option('--volume',
              required=True,
              type=click.STRING,
              help='The named volume where the zip is to be uploaded. for eg. /my_saved_volume.tar.gz ')
@click.option('--path',
              required=True,
              type=click.Path(exists=True,
                              file_okay=True,
                              dir_okay=False,
                              resolve_path=True,
                              readable=True),
              help='The path to load the zip or tar or tar.gz from.')
@click.option('--interactive',
              default='True',
              type=click.BOOL,
              help='Run the script interactively')
def load(volume, path, interactive):
    """Load the locally saved volume to named docker-volume."""
    path, filename = utils.get_filename_from_path(path)
    allowed, extension = utils.allowed_files(filename)
    extraction_command = utils.command_dict[extension]
    if not allowed:
        rwt('File extension not allowed', traceback=Ellipsis)

    load_cmd = utils.load_cmd.format(volume, path, extraction_command, filename)

    confirm_msg = 'The named volume already exists.\nDo you wish to overwrite?'
    if utils.docker_volume_exist(volume):
        click.confirm(confirm_msg, abort=True)

    if interactive:
        click.confirm('Safe to upload the named volume. Do you want to continue', abort=True)

    utils.execute_subprocess(load_cmd)

    msg = '\nSuccessfully imported docker volume at: {0} as {1}\n'.format(os.path.join(path, filename), volume)
    utils.echo(msg, color='green')
