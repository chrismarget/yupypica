# This program is placed into the public domain.
from os.path import dirname, isdir, join
from subprocess import check_output, CalledProcessError


def get_version():
    d = dirname(__file__)+"/../.."
    version = "v0.0.0-unknown"

    if isdir(join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git describe --tags --match v[0-9].*'.split()
        try:
            version = check_output(cmd, cwd=d).decode().strip()
        except CalledProcessError:
            return version

        # todo: check for comitted changes since last tag

        # Check for uncommitted changes
        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            working = check_output(cmd).decode().strip()
        except CalledProcessError:
            return version

        if working != '':
            version += '-working'

    return version
