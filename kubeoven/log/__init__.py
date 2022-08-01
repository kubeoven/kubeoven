from colored import fg, stylize
import sys

prefix = {"hostname": "localhost"}


def info(message: str, hostname: str = ""):
    print_msg(message, "info", fg(40), hostname)


def warn(message: str, hostname: str = ""):
    print_msg(message, "warn", fg(11), hostname)


def error(message: str, hostname: str = ""):
    print_msg(message, "error", fg("red"), hostname)


def print_msg(message: str, type: str, color: str, hostname: str = ""):
    node = stylize(hostname or prefix["hostname"], fg(39))
    level = stylize(type, color)
    out = "[%s] [%s]: %s" % (node, level, message)
    print(out, file=sys.stderr)


def set_hostname(node: str):
    prefix["hostname"] = node
