from __future__ import annotations

import os
import numpy

from typing import Tuple, Callable, Union

from amulet.api.block import BlockManager
from amulet.api.chunk import Chunk
from amulet.world_interface.loader import Loader
import PyMCTranslate
from PyMCTranslate.py3.translation_manager import Version

SUPPORTED_TRANSLATOR_VERSION = 0
SUPPORTED_META_VERSION = 0

TRANSLATORS_DIRECTORY = os.path.dirname(__file__)

loader = Loader(
    "translator",
    TRANSLATORS_DIRECTORY,
    SUPPORTED_META_VERSION,
    SUPPORTED_TRANSLATOR_VERSION,
)


class Translator:
    def _translator_key(
        self, version_number: Union[int, Tuple[int, int, int]]
    ) -> Tuple[str, Union[int, Tuple[int, int, int]]]:
        """
        Return the version key for PyMCTranslate

        :return: The tuple version key for PyMCTranslate
        """
        raise NotImplementedError()

    @staticmethod
    def is_valid(key: Tuple) -> bool:
        """
        Returns whether this translator is able to translate the chunk type with a given identifier key,
        generated by the decoder.

        :param key: The key who's decodability needs to be checked.
        :return: True if this translator is able to translate the chunk type associated with the key, False otherwise.
        """
        raise NotImplementedError()

    def to_universal(
        self,
        game_version: Union[int, Tuple[int, int, int]],
        translation_manager: PyMCTranslate.TranslationManager,
        chunk: Chunk,
        palette: numpy.ndarray,
        callback: Callable,
        full_translate: bool,
    ) -> Tuple[Chunk, numpy.ndarray]:
        """
        Translate an interface-specific chunk into the universal format.

        :param game_version: The version number (int or tuple) of the input chunk
        :param translation_manager: PyMCTranslate.TranslationManager used for the translation
        :param chunk: The chunk to translate.
        :param palette: The palette that the chunk's indices correspond to.
        :param callback: function callback to get a chunk's data
        :param full_translate: if true do a full translate. If false just unpack the palette (used in callback)
        :return: Chunk object in the universal format.
        """
        raise NotImplementedError

    def from_universal(
        self,
        max_world_version_number: Union[int, Tuple[int, int, int]],
        translation_manager: PyMCTranslate.TranslationManager,
        chunk: Chunk,
        palette: numpy.ndarray,
        callback: Union[Callable, None],
        full_translate: bool,
    ) -> Tuple[Chunk, numpy.ndarray]:
        """
        Translate a universal chunk into the interface-specific format.

        :param max_world_version_number: The version number (int or tuple) of the max world version
        :param translation_manager: PyMCTranslate.TranslationManager used for the translation
        :param chunk: The chunk to translate.
        :param palette: The palette that the chunk's indices correspond to.
        :param callback: function callback to get a chunk's data
        :param full_translate: if true do a full translate. If false just pack the palette (used in callback)
        :return: Chunk object in the interface-specific format and palette.
        """
        raise NotImplementedError


if __name__ == "__main__":
    import time

    print(loader.get_all())
    time.sleep(1)
    loader.reload()
    print(loader.get_all())
