#!/usr/bin/env python


from cuckoo.utils.imports import import_submodules

import_submodules(locals(), __name__, __path__)


def main():
    import os
    os.environ.setdefault('FLASK_APP', 'cuckoo.app')

    from .base import cli
    cli.main()
