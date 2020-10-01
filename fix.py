import configparser
import os

from pyutil.subcommand import Subcommand
import argparse
import shlex

from save import get_current_display_settings, get_config_name


class Fix(Subcommand):
    NAME = 'fix'

    def on_parser_init(self, parser: argparse.ArgumentParser):
        pass

    def on_command(self, args):
        cp = configparser.ConfigParser()

        if os.path.isfile(args.config):
            cp.read(args.config)
        else:
            print('error: could not load config from ' + str(args.config))
            return

        ds = get_current_display_settings(args.displayplacer)

        name = get_config_name(ds)

        if not cp.has_section(name):
            print('error: could not load config for displays ' + str(name))
            return

        print('resetting displays ...', end='', flush=True)
        args.displayplacer(list(cp[name].values()))
        print('done')

