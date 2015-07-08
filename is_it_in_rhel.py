# -*- coding: utf-8 -*-

"""
# is-it-in-rhel: a command line tool to check if something is packaged in
#                RHEL
#
# Copyright (C) 2015 Red Hat Inc
# Author: Pierre-Yves Chibon <pingou@pingoured.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
# See http://www.gnu.org/copyleft/gpl.html  for the full text of the
# license.
"""

import argparse
import requests

__version__ = '1.0'


class IsItInRhelError(Exception):
    ''' This class is raised when an error occurs in this script. '''
    pass


def get_rhel_json(release):
    ''' For a specified release of RHEL, retrieve the JSON file at
    https://infrastructure.fedoraproject.org/repo/json/
    '''
    url = 'https://infrastructure.fedoraproject.org/repo/json/pkg_el{rel}.json'
    req = requests.get(url.format(rel=release))
    if req.status_code == 404:
        raise IsItInRhelError(
            'No information could be found about this RHEL release: %s' % (
                release))
    elif req.status_code != 200:
        raise IsItInRhelError(
            'Something went wrong when retrieving information about this '
            'RHEL release: %s, if the problem persists, contact an '
            'admin.' % (release))

    data = None
    try:
        data = req.json()
    except:
        raise IsItInRhelError(
            'No JSON data found in the information retrieved about this '
            'RHEL release: %s, if the problem persists, contact an '
            'admin.' % (release))

    return data


def get_rhel_releases():
    ''' Returns the list of RHEL releases available at
    https://infrastructure.fedoraproject.org/repo/json/
    '''
    req = requests.get('https://infrastructure.fedoraproject.org/repo/json/')
    releases = []
    for row in req.text.split('\n'):
        if 'pkg_el' in row:
            rel = row.split('pkg_el', 1)[1].split('.json')[0]
            releases.append(rel)

    return releases


def _show_pkg_info(pkg, release, data, with_channel=False):
    ''' Show information about a specific package. '''
    tmpl = '{pkg} is in RHEL {rel};   version: {ver};   arch{arch}'

    if with_channel:
        tmpl += ';   channel{chan}'

    if len(data['arch']) > 1:
        arch = 's: {0}'.format(', '.join(sorted(data['arch'])))
    else:
        arch = ': {0}'.format(data['arch'][0])

    if len(data['channel']) > 1:
        channel = 's: {0}'.format(', '.join(sorted(data['channel'])))
    else:
        channel = ': {0}'.format(data['channel'][0])

    print(tmpl.format(
        pkg=pkg,
        rel=release,
        ver=data['version'],
        arch=arch,
        chan=channel,
    ))


def check_pkg_in_rhel(pkg, releases, with_channel=False, search=False):
    ''' Checks if a given package in present in the specified RHEL releases.
    '''
    if not isinstance(releases, (tuple, set, list)):
        releases = [releases]

    for release in releases:
        try:
            data = get_rhel_json(release)
        except IsItInRhelError as err:
            print(err)
            return

        found = False
        if not search and pkg in data['packages']:
            found = True
            _show_pkg_info(
                pkg, release, data['packages'][pkg],
                with_channel=with_channel)

        elif search:
            for pk in data['packages']:
                if pkg.lower() in pk.lower():
                    found = True
                    _show_pkg_info(
                        pk, release, data['packages'][pk],
                        with_channel=with_channel)


        if not found:
            print('{pkg} is not in RHEL {rel}'.format(pkg=pkg, rel=release))


def setup_parser():
    '''
    Set the main arguments.
    '''
    parser = argparse.ArgumentParser(prog="is-it-in-rhel")
    # General connection options
    parser.add_argument('--version', action='version',
                        version='is-it-in-rhel %s' % (__version__))

    parser.add_argument('--channel', action='store_true', default=False,
                        help='Show in which channel the package can be found')
    parser.add_argument('--search', action='store_true', default=False,
                        help='Search (case-insensitive) the package '
                             'specified in the list of packages instead of '
                             'doing a perfect match search.')
    parser.add_argument('--release', default='all',
                        help='RHEL release to check, defaults to `all`')

    parser.add_argument('pkg', help="Package name to search in RHEL")

    return parser



def main():
    ''' Main function '''
    # Set up parser for global args
    parser = setup_parser()
    # Parse the commandline
    try:
        arg = parser.parse_args()
    except argparse.ArgumentTypeError, err:
        print "\nError: {0}".format(err)
        return 2

    return_code = 0
    releases = arg.release
    if arg.release == 'all':
        releases = get_rhel_releases()

    check_pkg_in_rhel(
        arg.pkg, releases, with_channel=arg.channel, search=arg.search)

    return return_code


if __name__ == '__main__':
    main()
