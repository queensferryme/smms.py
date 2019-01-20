'''Command line toolkit for managing images at https://sm.ms'''

import json
from glob import glob

import click

from .api import Api
from .history import History
from .utils import error, success, warning

class AliasedGroup(click.Group):
    '''Creating abbreviations for commands'''
    def get_command(self, ctx, cmd_name):
        aliases = {'d': 'delete', 's': 'search', 'u': 'upload'}
        cmd_name = aliases[cmd_name] if cmd_name in aliases else cmd_name
        return super().get_command(ctx, cmd_name)

@click.group(cls=AliasedGroup)
def cli():
    pass

@cli.command('delete')
@click.argument('filenames', nargs=-1)
@click.option('--comment', '-c', help='wildcard statement for matching commentations')
@click.option('--date', '-d', multiple=True,
              help='one or more date strings like "yyyy-mm-dd" to specify search scope')
@click.option('--yes', '-y', is_flag=True, help='delete without confirmation')
def delete(filenames, comment, date, yes):
    '''delete images from remote server & clean local history'''
    records = list(History().filter(filenames, comment, date))
    if not records:
        click.echo('{}: no match found'.format(warning('WARNING')))
    else:
        for record in records:
            # confirm before delete
            if not yes and \
               not click.confirm('delete {0[filename]}({0[comment]})'.format(record)):
                record['fail'] = True
                continue
            # delete an image
            if Api.delete(record['delete']):
                click.echo('{}: {} successfully deleted'
                           .format(success('SUCCESS'), record['filename']))
            else:
                record['fail'] = True
                click.echo('{}: {} failed to delete'
                           .format(error('ERROR'), record['filename']))
        History().delete(record['delete'] for record in records if 'fail' not in record)

@cli.command('migrate')
def migrate():
    '''migrate local history from version 0.0.2 to 1.0.0'''
    History().migrate()

@cli.command('search')
@click.argument('filenames', nargs=-1)
@click.option('--comment', '-c', help='wildcard statement for matching commentations')
@click.option('--date', '-d', multiple=True,
              help='one or more date strings like "yyyy-mm-dd" to specify search scope')
def search(filenames, comment, date):
    '''search for matched records in local history'''
    records = tuple(History().filter(filenames, comment, date))
    if not records:
        click.echo('{}: no match found'.format(warning('WARNING')))
    else:
        click.echo('{}: {} matches found'.format(success('SUCCESS'), len(records)))
        for index, record in enumerate(records, 1):
            click.echo('{}: {}'.format(warning('[{}]'.format(index)), record))

@cli.command('upload')
@click.argument('filename', nargs=1)
@click.option('--comment', '-c', default='', help='commentation string for images')
def upload(filename, comment):
    '''upload images & insert new records into local history'''
    images = glob(filename)
    if not images:
        click.echo('{}: no image to upload'.format(warning('WARNING')))
    for image in images:
        # upload an image
        resp = json.loads(Api.upload(image))
        # update local history
        if resp['code'] == 'error':
            click.echo('{}: {}', error('ERROR'), resp['msg'].lower())
        else:
            History().insert({
                'filename': resp['data']['filename'],
                'url': resp['data']['url'],
                'delete': resp['data']['delete'],
                'comment': comment
            })
            click.echo('{}: image {} upload success, url {}'
                       .format(success('SUCCESS'), resp['data']['filename'], resp['data']['url']))
