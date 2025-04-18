import json
import sys
from subprocess import check_output

from importlib.metadata import version, PackageNotFoundError


def get_version():
    out = check_output("gauge -v --machine-readable",shell=True)
    data = json.loads(str(out.decode()))
    for plugin in data['plugins']:
        if plugin['name'] == 'python':
            return plugin['version']
    return ''

def install_getgauge(getgauge_version):
    install_cmd = [sys.executable, "-m", "pip", "install", getgauge_version]
    if not in_venv():
        install_cmd.append("--user")
    if "dev" in getgauge_version:
        install_cmd.append("--pre")
    check_output([" ".join(install_cmd)], shell=True)

def in_venv():
    return sys.prefix != sys.base_prefix

def assert_versions():
    python_plugin_version = get_version()
    if not python_plugin_version:
        print('The gauge python plugin is not installed!')
        exit(1)

    expected_gauge_version = python_plugin_version

    try:
        getgauge_version = version('getgauge')
        if getgauge_version != expected_gauge_version:
            install_getgauge("getgauge=="+expected_gauge_version)
    except PackageNotFoundError:
        install_getgauge("getgauge=="+expected_gauge_version)


if __name__ == '__main__':
    assert_versions()
