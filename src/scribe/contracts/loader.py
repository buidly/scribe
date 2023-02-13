import pathlib
from typing import Any

import toml
import yaml
from multiversx_sdk_cli import utils

from scribe import settings
from scribe.constants import EnvironmentType

from . import exceptions, info


def is_workspace(path: pathlib.Path) -> bool:
    """Check if path is workspace"""

    return any([file.name in settings.WORKSPACE_FILE_NAME for file in path.iterdir()])


def is_contract(path: pathlib.Path) -> bool:
    """Check if path is contract"""

    return any([file.name in settings.CONTRACT_ROOT_FILE for file in path.iterdir()])


def load_workspace(path: pathlib.Path) -> info.WorkspaceContracts:
    """Load rust workspace contracts

    :raise WorkspaceNotFound: If path is not a workspace
    :raise ContractCargoNotFound: If Cargo.toml file not found
    :raise ContractCargoInvalid: If Cargo.toml file is invalid
    """

    if not is_workspace(path):
        raise exceptions.WorkspaceNotFound

    contracts: list[info.SmartContractData] = []
    for file in path.iterdir():
        if not file.is_dir() or not is_contract(file):
            continue

        try:
            contract_info = toml.load(file / settings.RUST_CARGO_FILE)
        except FileNotFoundError:
            raise exceptions.ContractCargoNotFound
        except TypeError:
            raise exceptions.ContractCargoInvalid

        contracts.append(info.SmartContractData(**contract_info.get("package", {}), contract_path=file))

    return info.WorkspaceContracts(contracts=contracts)


def load_deploy_config(root: pathlib.Path, env: EnvironmentType) -> dict[str, Any]:
    deploy_config_file = root / settings.INTERACTIONS_DIR_NAME / settings.DEPLOY_CONFIG_NAME

    if not deploy_config_file.exists():
        raise exceptions.MissingDeployConfigFile()

    return yaml.load(deploy_config_file.read_text(), Loader=yaml.FullLoader)


def load_bytecode(sc_data: info.SmartContractData) -> str:
    bytecode_file = sc_data.contract_path / settings.OUTPUT_DIR_NAME / f"{sc_data.name}.{settings.BYTECODE_TYPE}"

    if not bytecode_file.exists():
        raise exceptions.MissingBytecodeFile()

    try:
        return utils.read_binary_file(bytecode_file).hex()
    except Exception:
        raise exceptions.CouldNotLoadBytecode()
