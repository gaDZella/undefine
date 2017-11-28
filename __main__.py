import os
import argparse
from SharpCleaner import SharpCleaner


def test(p_args):
    print("Checking for applying the following name definitions:")
    _show_report(_do_clean(p_args, False),
                 "{0} code lines to remove. {2} total number of lines to remove. {1} files affected")


def apply(p_args):
    print("Applying the following name definitions:")
    _show_report(_do_clean(p_args, True),
                 "{0} code lines removed. {2} total number of lines removed. {1} files affected")


def _do_clean(p_args,  apply_changes):
    defined = p_args.define if p_args.define is not None else []
    undefined = p_args.undef if p_args.undef is not None else []
    keys = dict([(n, True) for n in defined] + [(n, False) for n in undefined])
    for name, value in keys.items():
        print(str.format("#{0} {1}", 'define' if value else 'undef', name))
    print('...', end='\r')
    cleaner = SharpCleaner(keys)
    return cleaner.clean(p_args.path, apply_changes)


def _show_report(results, completed_report_format_string):
    code_lines = 0
    total_lines = 0
    files_count = 0
    error_files = []
    for result in results:
        if result is not None:
            if result.error is not None:
                error_files.append(result.file)
            else:
                code_lines += result.code_lines
                total_lines += result.total_lines
                if result.total_lines > 0:
                    files_count += 1
    print(str.format("Complete. " + completed_report_format_string,
                     code_lines, files_count, total_lines))
    if len(error_files) > 0:
        print("Failed to process these files:")
        for file in error_files:
            print(file)


def _add_name_definition_args(p):
    p.add_argument('-d', '--define', action='append', metavar='name', help='preprocessor name to define.')
    p.add_argument('-u', '--undef', action='append', metavar='name', help='preprocessor name to undefine.')


def _add_working_path_args(p):
    p.add_argument('path', default=os.getcwd(), metavar='path', nargs='?',
                        help='working path, current working folder by default')


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

parser_check = subparsers.add_parser('check', help='Processes files and shows results without applying changes.')
_add_name_definition_args(parser_check)
_add_working_path_args(parser_check)
parser_check.set_defaults(act=test)

parser_clean = subparsers.add_parser('apply', help='Processes files, shows results, and applies changes.')
_add_name_definition_args(parser_clean)
_add_working_path_args(parser_clean)
parser_clean.set_defaults(act=apply)

args = parser.parse_args()
if hasattr(args, 'act'):
    args.act(args)




