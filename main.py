'''
A command line toolkit for uploading images at https://sm.ms
'''

import datetime
import json
import os
from fnmatch import fnmatch
from glob import glob
from pathlib import Path

import click
import requests

# Define constant variables
COLORS = {
    'WARNING': lambda s: '\033[0;33;40m{}\033[0m'.format(s),
    'FAIL': lambda s: '\033[0;31;40m{}\033[0m'.format(s),
}
HISTORY = os.path.join(str(Path.home()), '.sm.ms.history')

# Define public functions
def parse_pattern(pattern):
    '''
    Function to parse pattern string
    '''

    pattern = [each.strip() for each in pattern.split(':', 1)]
    if len(pattern) != 2 or \
        pattern[0] not in ('filename', 'url', 'delete', 'comment'):
        click.echo(COLORS['FAIL']('ERROR: wrong pattern'))
        exit()
    return pattern

def extract_history(history, dates):
    '''
    Function to extract snapshots from `history` object
    '''

    snapshots = []
    # No specific dates
    if not dates:
        snapshots = list(flatten_history(history))
    # Create list of specific dates
    for date in dates:
        if date not in history:
            click.echo(COLORS['WARNING']('WARNING: no commit on {}'.format(date)))
        else:
            snapshots.extend(history[date])
    return snapshots

def load_history():
    '''
    Function to load history from `.sm.ms.history`
    '''

    # Create a new file if not existed
    if not os.path.exists(HISTORY):
        with open(HISTORY, 'wt'):
            pass
    # Read history file, handle empty history
    with open(HISTORY, 'rt', encoding='utf-8') as fin:
        history = fin.read()
        history = history if history else '{}'
    # parse history with module json
    try:
        history = json.loads(history)
    except json.JSONDecodeError:
        click.echo(COLORS['FAIL']('ERROR: corrupted history file'))
        exit()
    return history

def flatten_history(history):
    '''
    Function to flatten the `history` object as a generator
    '''

    for array in history.values():
        yield from array

# Define command line utilities
@click.group()
def cli():
    pass

@cli.command('clear')
def clear_history():
    '''
    Clear upload history on server
    '''

    requests.get('https://sm.ms/api/clear')
    click.echo('INFO: clear success!')

@cli.command('upload')
@click.argument('images', nargs=-1, type=click.Path())
@click.option('--comment', '-c', default='--- NO COMMENT ---',
              help='commentation strings, making comments for images')
def upload_images(images, comment):
    '''
    Upload images and record commits, shell-style wildcards supported
    '''

    UPLOAD_PARAMS = {'format': 'json', 'ssl': True}
    UPLOAD_URL = 'https://sm.ms/api/upload'

    def __glob(patterns):
        '''
        Function to find all matched images
        '''

        for pattern in patterns:
            yield from (image for image in glob(pattern) if os.path.isfile(image))

    def __upload(images):
        '''
        Function to upload images, work as a generator
        '''

        images = list(__glob(images))
        for image in images:
            # Start a HTTP request
            files = {'smfile': open(image, 'rb')}
            resp = requests.post(UPLOAD_URL, files=files, params=UPLOAD_PARAMS)
            status = json.loads(resp.text)
            # Handle success or failure
            if status['code'] == 'success':
                click.echo('INFO: {} upload success! url at {}' \
                           .format(os.path.abspath(image), status['data']['url']))
                yield status
            else:
                click.echo(COLORS['FAIL']('ERROR: {} upload failed!' \
                           .format(os.path.abspath(image))))
                click.echo(COLORS['WARNING']('WARNING: {}' \
                           .format(status['msg'])))
        # User notification
        if not images:
            click.echo(COLORS['WARNING']('WARNING: nothing to upload!'))

    def __cache(statuses, comment):
        '''
        Function to cache history requests
        '''

        history = load_history()
        # Update .sm.ms.history file
        for status in statuses:
            isodate = datetime.date.fromtimestamp(status['data']['timestamp']).isoformat()
            info = {
                'filename': status['data']['filename'],
                'url': status['data']['url'],
                'delete': status['data']['delete'],
                'comment': comment
            }
            history.setdefault(isodate, []).append(info)
        with open(HISTORY, 'wt', encoding='utf-8') as fout:
            fout.write(json.dumps(history, ensure_ascii=False, indent=4))

    # Main upload procedure
    statuses = __upload(images)
    __cache(statuses, comment)

@cli.command('query')
@click.option('--dates', '-d', multiple=True,
              help='ISO date strings, specifying dates to query')
@click.option('--pattern', '-p', nargs=1,
              help='Search pattern, like <property>:<shell-style wildcards>')
def query_images(dates, pattern):
    '''
    Query records from local history
    '''

    # Variables initialized
    history = load_history()
    pattern = parse_pattern(pattern) if pattern else None
    snapshots = extract_history(history, dates)
    # Filter by pattern
    if pattern:
        snapshots = [each for each in snapshots if fnmatch(each[pattern[0]], pattern[1])]
    # Handle no-match-found
    if not snapshots:
        click.echo(COLORS['WARNING']('WARNING: nothing found!'))
        exit()
    # Output query results
    click.echo(COLORS['WARNING']('QUERY RESULTS:'))
    for index, snapshot in enumerate(snapshots):
        click.echo('[{}]: {}'.format(index, snapshot))

@cli.command('delete')
@click.option('--All', '-A', is_flag=True,
              help='ALL flag, indicating deleting all images')
@click.option('--dates', '-d', multiple=True,
              help='ISO date strings, specifying dates to delete')
@click.option('--pattern', '-p', nargs=1,
              help='Search pattern, like <property>:<shell-style wildcards>')
@click.confirmation_option(help='Confirm delete events')
def remove_images(all, dates, pattern):
    '''
    Remove specific images from server
    '''

    def __uncache(urls):
        '''
        Remove history record according to urls
        '''

        nonlocal history
        for key in history:
            history[key] = [item for item in history[key] if item['url'] not in urls]
        # Remove empty dictionaries
        history = {key: value for key, value in history.items() if history[key]}
        with open(HISTORY, 'wt', encoding='utf-8') as fout:
            fout.write(json.dumps(history, ensure_ascii=False, indent=4))

    # Variables initialized
    history = load_history()
    if not history:
        click.echo(COLORS['WARNING']('WARNING: empty history file!'))
        exit()
    pattern = parse_pattern(pattern) if pattern else None
    urls = []
    # Create snapshots
    snapshots = extract_history(history, dates)
    if pattern:
        snapshots = [each for each in snapshots if fnmatch(each[pattern[0]], pattern[1])]
    elif not all:
        for index, snapshot in enumerate(snapshots):
            click.echo('[{}]: {}'.format(index, snapshot))
        click.echo(COLORS['WARNING']('Which would you like to remove? [index/q to quit]: '))
        try:
            index = input()
            index = exit() if index.lower() == 'q' else int(index)
        except ValueError:
            click.echo(COLORS['FAIL']('ERROR: expect an integar!'))
            exit()
        else:
            snapshots = [snapshots[index]]
    # If nothing found
    if not snapshots:
        click.echo(COLORS['WARNING']('WARNING: nothing found!'))
    # Deleting all images in `snapshots` object
    for snapshot in snapshots:
        urls.append(snapshot['url'])
        requests.get(snapshot['delete'])
        click.echo('INFO: remove {} at {}'
                   .format(snapshot['filename'], snapshot['url']))
    __uncache(urls)
    click.echo('INFO: remove completed!')
