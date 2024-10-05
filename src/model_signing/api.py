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

from model_signing.manifest import manifest
from model_signing.serialization import serialization
from model_signing.serialization import serialize_by_file


# TODO: use PathLike!!
def hash(model_path: str | pathlib.Path) -> manifest.Manifest:
    """Hashes a model using the default configuration.

    Hashing is the common part of signing and signature verification. It is
    extracted to a separate method for reuse and to enable benchmarking, since
    this is the part that takes most of the time when performing signing.

    Since we need to be flexible on the serialization format, this returns a
    manifest, instead of just a single digest. The type of returned manifest
    depends on the configuration.

    Args:
        model_path: the path to the model to hash.

    Returns:
        A manifest that represents hashes for the model.
    """
    return HashingConfig().hash(model_path)


class HashingConfig:
    """Configuration to use when hashing models.

    To be flexible, we don't directly compute a single digest for the model.
    Instead, we serialize the model to a manifest representation -- a pairing
    between model components and their corresponding hashes. A manifest could be
    a single digest for the entire model, a record of all files with their
    associated digests, a record of file shards with their associated digests or
    any other supported configuration.  It is also possible to have manifests of
    a mixed granularity, if the library supports them. Consult each individual
    method in this class to determine the type of the manifest being used.

    For a hashing configuration we need to establish the manifest type (as
    mentioned in the previous paragraph) and the hashing algorithm used to hash
    individual objects in the manifest. If a serialization method needs
    additional hashing methods, they are configured in the corresponding setter.

    We also need to configure the list of files from within the model directory
    that should be ignored (if any). This is useful to skip hashing files that
    don't impact model behavior, as a minor performance gain.

    The default hashing configuration uses SHA256 to compute the digest of every
    file in the model. The resulting manifest is a listing of files paired with
    their hashes. By default, no file is ignored.

    Users can use the `set_*` methods to select other options that are supported
    by the library.
    """

    def __init__(self):
        """Initializes the default configuration for hashing."""
        self._ignored_paths = frozenset()
        pass

    def hash(self, model_path: str | pathlib.Path) -> manifest.Manifest:
        """Hashes a model using the current configuration."""
        model_path = pathlib.Path(model_path)
        raise ValueError("yadda yadda")

    def set_ignored_paths(
        self, paths: Iterable[str | pathlib.Path] = frozenset()
    ) -> Self:
        """Configures the paths to be ignored during serialization of a model.

        If the model is a single file, there are no paths that are ignored. If
        the model is a directory, all paths must be within the model directory.
        If a path to be ignored is absolute, we convert it to a path within the
        model directory during serialization. If the path is relative, it is
        assumed to be relative to the model root.

        If a path is a directory, serialization will ignore both the path and
        any of its children.

        Args:
            paths: the paths to ignore

        Returns:
            The new hashing configuration with a new set of ignored paths.
        """
        self._ignored_paths = frozenset({pathlib.Path(p) for p in paths})
        return self


#def sign(model_path: str | pathlib.Path):
#    """Signs a model using the default configuration.
#
#    Args:
#        model_path: the path to the model to sign.
#    """
#    SigningConfig().sign(model_path)
#
#
#def verify():
#    """Verifies the signature for a model."""
#    pass  # TODO
#
#
#class SigningConfig:
#    """Configuration to use when signing models.
#
#    We need to configure:
#      - signer to use: Sigstore, PKI, etc.
#      - signature format: in-toto (multiple formats), digest, etc.
#      - serialization method: converting from a model to a `manifest.Manifest`
#      - hashing algorithms
#
#    All of these have a default value, but users can use the `set_*` methods to
#    select other options that are supported by the library.
#    """
#
#    def __init__(self):
#        """Initializes the default configuration for signing."""
#        self._ignored_paths = frozenset()
#        self._serializer = seri
#
#    def sign(self, model_path: str | pathlib.Path):
#        """Signs a model using the current configuration.
#
#        Args:
#            model_path: the path to the model to sign.
#        """
#        model_path = pathlib.Path(model_path)
#
#        # TODO: rest of signing
#
