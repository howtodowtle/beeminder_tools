import subprocess
import sys


def check_if_package_installed(package_name):
    """Checks if a package is installed in the current environment."""
    try:
        __import__(package_name)
    except ImportError:
        return False
    else:
        return True


def install_package(package_name):
    """Installs a package in the current environment."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def install_packages_if_not_installed(package_list, debug=False):
    """For each package in a list of packages,
    checks if a package is installed in the current environment and installs it if not.
    """
    if debug:
        print(f"Trying to install {package_list}")
    if isinstance(package_list, str):
        package_list = [package_list]
    for package_name in package_list:
        if not check_if_package_installed(package_name):
            print(f"Package '{package_name}' not installed. Installing...")
