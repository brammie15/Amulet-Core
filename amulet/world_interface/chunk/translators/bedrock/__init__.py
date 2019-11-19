from __future__ import annotations

import numpy

from typing import Tuple, Callable, Union, List

from amulet.api.chunk import Chunk
from amulet.api.block import Block
from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity
from amulet.world_interface.chunk.translators import Translator
import PyMCTranslate


class BaseBedrockTranslator(Translator):
    def _translator_key(
        self, version_number: Tuple[int, int, int]
    ) -> Tuple[str, Tuple[int, int, int]]:
        return "bedrock", version_number

    def to_universal(
        self,
        game_version: Tuple[int, int, int],
        translation_manager: PyMCTranslate.TranslationManager,
        chunk: Chunk,
        palette: numpy.ndarray,
        callback: Callable,
        full_translate: bool,
    ) -> Tuple[Chunk, numpy.ndarray]:
        # Bedrock does versioning by block rather than by chunk.
        # As such we can't just pass in a single translator.
        # It needs to be done dynamically.
        versions = {}

        def translate(
            input_object: Union[Tuple[Tuple[Union[Tuple[int, int, int], None], Block], ...], Entity],
            get_block_callback: Callable[[Tuple[int, int, int]], Tuple[Block, Union[None, BlockEntity]]] = None
        ) -> Tuple[Block, BlockEntity, List[Entity], bool]:
            final_block = None
            final_block_entity = None
            final_entities = []
            final_extra = False

            if isinstance(input_object, Entity):
                # TODO: entity support
                pass

            elif isinstance(input_object, tuple):
                for depth, block in enumerate(input_object):
                    game_version_, block = block
                    if game_version_ is None:
                        if "block_data" in block.properties:
                            # if block_data is in properties cap out at 1.12.x
                            game_version_ = min(game_version, (1, 12, 999))
                        else:
                            game_version_ = game_version
                    version_key = self._translator_key(game_version_)
                    translator = versions.setdefault(version_key, translation_manager.get_version(*version_key).get().to_universal)
                    output_object, output_block_entity, extra = translator(block, get_block_callback)

                    if isinstance(output_object, Block):
                        if __debug__ and not output_object.namespace.startswith('universal'):
                            print(f'Error translating {block.blockstate} to universal. Got {output_object.blockstate}')
                        if final_block is None:
                            final_block = output_object
                        else:
                            final_block += output_object
                        if depth == 0:
                            final_block_entity = output_block_entity


                    elif isinstance(output_object, Entity):
                        final_entities.append(output_object)
                        # TODO: offset entity coords

                    final_extra |= extra

            return final_block, final_block_entity, final_entities, final_extra

        version = translation_manager.get_version(*self._translator_key(game_version))
        palette = self._unpack_palette(version, palette)
        chunk.biomes = self._biomes_to_universal(version, chunk.biomes)
        return self._translate(
            chunk, palette, callback, translate, full_translate
        )
