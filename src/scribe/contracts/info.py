from dataclasses import dataclass
from pathlib import Path

from . import exceptions


@dataclass
class SmartContractData:
    name: str
    version: str
    authors: list[str]
    edition: str
    publish: bool
    contract_path: Path
    bytecode: None | bytes = None


@dataclass
class WorkspaceContracts:
    contracts: list[SmartContractData]

    def get(self, contract_name: str) -> SmartContractData:
        """Gets contract from workspace

        Raises:
            ContractNotFound: If contract not found
        """
        for contract in self.contracts:
            if contract.name == contract_name:
                return contract

        raise exceptions.ContractNotFound
