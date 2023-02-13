import pathlib

import github
import typer
from multiversx_sdk_cli import accounts
from multiversx_sdk_network_providers import proxy_network_provider

from . import exceptions, repo, settings, wallet
from .constants import EnvironmentType


def build_account_from_pem(pem_path: pathlib.Path) -> accounts.Account:
    """Loads and syncs account from pem file"""
    if not pem_path.exists():
        raise FileNotFoundError(pem_path)

    proxy = proxy_network_provider.ProxyNetworkProvider(settings.PROXY)
    account = accounts.Account(pem_file=pem_path.as_posix())
    account.sync_nonce(proxy)

    return account


def build_account_from_repo(repo_name: str, env: EnvironmentType) -> accounts.Account:
    """Fetches the default pem file from a repo and builds an account from it"""
    gh_client = repo.init_github()
    repository = repo.get_repository(gh_client, repo_name)

    try:
        default_pem_file = repository.get_contents(f"{env.value}/{settings.DEFAULT_REPO_WALLET_FILE_NAME}")
    except github.UnknownObjectException:
        raise exceptions.PemFileForEnvNotFound()

    if isinstance(default_pem_file, list):
        raise exceptions.PemFileForEnvNotFound()

    raw_content = default_pem_file.decoded_content.decode("utf-8")

    if not settings.TMP_PATH_FOR_WALLET.exists():
        settings.TMP_PATH_FOR_WALLET.mkdir()
    with open(settings.TMP_PATH_FOR_WALLET / settings.DEFAULT_REPO_WALLET_FILE_NAME, "w") as f:
        f.write(raw_content)

    account = wallet.build_account_from_pem(settings.TMP_PATH_FOR_WALLET / settings.DEFAULT_REPO_WALLET_FILE_NAME)
    (settings.TMP_PATH_FOR_WALLET / settings.DEFAULT_REPO_WALLET_FILE_NAME).unlink()
    settings.TMP_PATH_FOR_WALLET.rmdir()

    return account


def build_account_default() -> accounts.Account:
    """Builds an account from the default pem file in the MX SDK"""
    if not settings.MX_SDK_DIR_PATH.exists():
        raise exceptions.MxSdkNotFound()

    typer.confirm(
        f"No wallet file provided, using default test wallet [ {settings.DEFAULT_TEST_WALLET.name} ] ?", abort=True
    )

    return wallet.build_account_from_pem(settings.DEFAULT_TEST_WALLET)
