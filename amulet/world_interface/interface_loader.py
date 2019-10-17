from __future__ import annotations

import glob
import importlib
import json
import os

from typing import Tuple, AbstractSet, Dict

from .interfaces.interface import Interface
from ..api import paths
from ..api.errors import InterfaceLoaderNoneMatched

_loaded_interfaces: Dict[str, Interface] = {}
_has_loaded_interfaces = False

SUPPORTED_INTERFACE_VERSION = 0
SUPPORTED_META_VERSION = 0

INTERFACES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'interfaces')


def _find_interfaces():
    """Load all interfaces from the interfaces directory"""
    global _has_loaded_interfaces

    directories = glob.iglob(os.path.join(INTERFACES_DIRECTORY, "*", ""))
    for d in directories:
        meta_path = os.path.join(d, "interface.meta")
        if not os.path.exists(meta_path):
            continue

        with open(meta_path) as fp:
            interface_info = json.load(fp)

        if interface_info["meta_version"] != SUPPORTED_META_VERSION:
            print(
                f'[Error] Couldn\'t enable interface located in "{d}" due to unsupported meta version'
            )
            continue

        if interface_info["interface"]["interface_version"] != SUPPORTED_INTERFACE_VERSION:
            print(
                f"[Error] Couldn't enable interface \"{interface_info['interface']['id']}\" due to unsupported interface version"
            )
            continue

        spec = importlib.util.spec_from_file_location(
            interface_info["interface"]["entry_point"],
            os.path.join(d, interface_info["interface"]["entry_point"] + ".py"),
        )
        modu = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modu)

        if not hasattr(modu, "INTERFACE_CLASS"):
            print(
                f"[Error] Interface \"{interface_info['interface']['id']}\" is missing the INTERFACE_CLASS attribute"
            )
            continue

        _loaded_interfaces[interface_info["interface"]["id"]] = modu.INTERFACE_CLASS()

        if __debug__:
            print(
                f"[Debug] Enabled interface \"{interface_info['interface']['id']}\", version {interface_info['interface']['wrapper_version']}"
            )

    _has_loaded_interfaces = True


def reload():
    """Reloads all interfaces"""
    _loaded_interfaces.clear()
    _find_interfaces()


def get_all_loaded_interfaces() -> AbstractSet[str]:
    """
    :return: The identifiers of all loaded interfaces
    """
    if not _has_loaded_interfaces:
        _find_interfaces()
    return _loaded_interfaces.keys()


def get_interface(identifier: Tuple) -> Interface:
    """
    Given an ``identifier`` will find a valid interface class and return it
    ("anvil", 1519)

    :param identifier: The identifier for the desired loaded interface
    :return: The class for the interface
    """
    interface_id = _identify(identifier)
    return _loaded_interfaces[interface_id]


def _identify(identifier: Tuple) -> str:

    if not _has_loaded_interfaces:
        _find_interfaces()

    for interface_name, interface_instance in _loaded_interfaces.items():
        if interface_instance.is_valid(identifier):
            return interface_name

    raise InterfaceLoaderNoneMatched("Could not find a matching interface")


if __name__ == "__main__":
    import time

    _find_interfaces()
    print(_loaded_interfaces)
    time.sleep(1)
    reload()
    print(_loaded_interfaces)
