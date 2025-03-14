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

"""The main entry-point for the library."""

import pathlib

import click


# Decorators for commonly used arguments and options
model_path_argument = click.argument(
    "model_path", type=pathlib.Path, metavar="MODEL_PATH"
)
signature_location_option = click.option(
    "--signature",
    type=pathlib.Path,
    default=pathlib.Path("./model.sig"),
    help="Location of the signature file. Defaults to ./model.sig.",
)


@click.group(
    epilog=(
        "Check https://sigstore.github.io/model-transparency for "
        "documentation and more details."
    )
)
def main():
    """ML model signing and verification."""
    print("OK")


@main.group(
    name="sign", invoke_without_command=True, subcommand_metavar="PKI_METHOD"
)
@click.pass_context
def _sign(ctx):
    """Sign models.

    Produces a cryptographic signature (in the form of a Sigstore bundle) for a
    model. We support any model format, either as a single file or as a
    directory.

    We support multiple PKI methods, specified as subcommands. By default, the
    signature is generated via Sigstore (sigstore subcommand). To see the help
    for each subcommand use the specific subcommand's `--help` option.
    """
    print("Signing mode...")
    if ctx.invoked_subcommand is None:
        ctx.invoke(_sign_sigstore)


@_sign.command(name="sigstore")
@model_path_argument
@signature_location_option
def _sign_sigstore(model_path: pathlib.Path, signature: pathlib.Path):
    """Sign using Sigstore (default signing method)."""
    print("Sigstore")


@_sign.command(name="private_key")
@model_path_argument
@signature_location_option
def _sign_private_key(model_path: pathlib.Path, signature: pathlib.Path):
    """Sign using a private key."""
    print("private key TODO")


@_sign.command(name="certificate")
@model_path_argument
@signature_location_option
def _sign_certificate(model_path: pathlib.Path, signature: pathlib.Path):
    """Sign using a certificate."""
    print("certificate TODO")


@_sign.command(name="skip")
@model_path_argument
@signature_location_option
def _sign_skip(model_path: pathlib.Path, signature: pathlib.Path):
    """Don't sign, just hash the model (use only for debugging)."""
    print("skip TODO")


@main.group(
    name="verify", invoke_without_command=True, subcommand_metavar="PKI_METHOD"
)
def _verify():
    """Verify models."""
    print("Verification mode...")


@_verify.command(name="sigstore")
def _verify_sigstore():
    """Verify using Sigstore (default signing method)."""
    print("Sigstore")


@_verify.command(name="private_key")
def _verify_private_key():
    """Verify using a private key."""
    print("private key")


@_verify.command(name="certificate")
def _verify_certificate():
    """Verify using a certificate."""
    print("certificate")


@_verify.command(name="skip")
def _verify_skip():
    """Don't sign, just hash the model (use only for debugging)."""
    print("skip")
