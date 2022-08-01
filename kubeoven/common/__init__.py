
def handle_extra_types(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


def to_amd(arch: str):
    if arch == 'x86_64':
        return 'amd64'
    return arch

