import argparse
import os


class ExtendedDefault(argparse.Action):
    def __init__(self, env_var, conf_parser, conf_section, conf_option, is_list, required=True, default=None, **kwargs):
        if env_var:
            if env_var in os.environ:
                if is_list:
                    default = os.environ[env_var].split(',')
                else:
                    default = os.environ[env_var]
            elif conf_parser and conf_section and conf_option:
                if conf_parser.has_option(conf_section, conf_option):
                    if is_list:
                        default = conf_parser.get(conf_section, conf_option).split(',')
                    else:
                        default = conf_parser.get(conf_section, conf_option)
        if required and default:
            required = False
        super(ExtendedDefault, self).__init__(default=default, required=required,
                                              **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
