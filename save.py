import configparser
import os

from pyutil.subcommand import Subcommand
import argparse
import shlex


def get_current_display_settings(displayplacer):
    ds = []
    for confline in shlex.split(str(displayplacer.list()).splitlines()[-1:][0])[1:]:
        confline: str
        for id in filter(lambda e: e.startswith('id:'), confline.split()):
            ds.append((id[len('id:'):], confline))

    return sorted(ds)


def get_config_name(display_settings):
    ids, configs = zip(*display_settings)
    return ':'.join(ids)


class Save(Subcommand):
    NAME = 'save'

    def on_parser_init(self, parser: argparse.ArgumentParser):
        pass

    def on_command(self, args):
        cp = configparser.ConfigParser()

        if os.path.isfile(args.config):
            cp.read(args.config)

        ds = get_current_display_settings(args.displayplacer)

        name = get_config_name(ds)

        for id, config in sorted(ds):
            if not cp.has_section(name):
                cp[name] = {}
            cp[name][id] = config

        if not os.path.isdir(os.path.dirname(args.config)):
            os.makedirs(os.path.dirname(args.config), exist_ok=True)

        with open(args.config, 'w+') as f:
            cp.write(f)

