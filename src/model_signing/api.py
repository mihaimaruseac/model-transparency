# Copyright 2024 The Sigstore Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Public, high-level API for the model_signing library.

Users should use this API to sign models and verify the model integrity instead
of reaching out to the internals of the library. We guarantee backwards
compatibility only for the API defined in this file.
"""

from collections.abc import Iterable
import pathlib
from typing import Self

from model_signing.serialization import serialization
from model_signing.serialization import serialize_by_file


def sign(model_path: str | pathlib.Path):
    """Signs a model using the default configuration.

    Args:
        model_path: the path to the model to sign.
    """
    SigningConfig().sign(model_path)


def verify():
    """Verifies the signature for a model."""
    pass  # TODO


class SigningConfig:
    """Configuration to use when signing models.

    We need to configure:
      - signer to use: Sigstore, PKI, etc.
      - signature format: in-toto (multiple formats), digest, etc.
      - serialization method: converting from a model to a `manifest.Manifest`
      - hashing algorithms

    All of these have a default value, but users can use the `set_*` methods to
    select other options that are supported by the library.
    """

    def __init__(self):
        """Initializes the default configuration for signing."""
        self._ignored_paths = frozenset()
        self._serializer = seri

    def sign(self, model_path: str | pathlib.Path):
        """Signs a model using the current configuration.

        Args:
            model_path: the path to the model to sign.
        """
        model_path = pathlib.Path(model_path)

        # TODO: rest of signing

    def set_ignored_paths(
        self, paths: Iterable[str | pathlib.Path] = frozenset()
    ) -> Self:
        """Configures the paths to be ignored during serialization of a model.

        If a path is a directory, itself and all of its children will be
        ignored.

        Args:
            paths: the paths to ignore

        Returns:
            The current instance, to support chaining configuration methods.
        """
        self._ignored_paths = frozenset({pathlib.Path(p) for p in paths})
        return self
