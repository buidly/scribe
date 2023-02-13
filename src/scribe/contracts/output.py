from dataclasses import dataclass
from enum import Enum, auto

import yaml
from multiversx_sdk_cli import accounts
from rich import print

from scribe import constants, settings

from . import info, loader


class DeploymentStatus(Enum):
    SUCCESS = auto()
    FAIL = auto()
    PENDING = auto()
    SIMULATED = auto()


@dataclass
class DeploymentResult:
    status: DeploymentStatus
    env: constants.EnvironmentType
    contract_data: info.SmartContractData
    contract_address: accounts.Address | None = None
    tx_hash: str | None = None

    def resolve(self) -> None:
        status_mapping = {
            DeploymentStatus.SUCCESS: self._resolve_success,
            DeploymentStatus.FAIL: self._resolve_fail,
            DeploymentStatus.SIMULATED: self._resolve_simulated,
        }

        status_mapping[self.status]()

    def _resolve_success(self) -> None:
        deploy_config_file = (
            self.contract_data.contract_path / settings.INTERACTIONS_DIR_NAME / settings.DEPLOY_CONFIG_NAME
        )
        deploy_config = loader.load_deploy_config(self.contract_data.contract_path, self.env)
        contract_deploy_info = deploy_config.get(self.env.value, {}).get(self.contract_data.name, {})
        contract_deploy_info[settings.DEFAULT_CONFIG_SC_ADDRESS_FIELD] = self.contract_address.bech32()  # type: ignore
        with open(deploy_config_file, "w") as file:
            yaml.dump(deploy_config, file)

        tx_url = settings.EXPLORER_TX_TEMPLATE.format(env=self.env.value, tx_hash=self.tx_hash)
        acc_url = settings.EXPLORER_ACCOUNT_TEMPLATE.format(env=self.env.value, address=self.contract_address)

        print(f"{settings.LOGGING_INFO_PREFIX} Tx Outcome: {tx_url}")
        print(f"{settings.LOGGING_INFO_PREFIX} Contract: {acc_url}")

    def _resolve_fail(self) -> None:
        # TODO: Add error handling
        pass

    def _resolve_simulated(self) -> None:
        # TODO: Add simulation handling
        pass
