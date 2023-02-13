import typer
from multiversx_sdk_cli import accounts, contracts, simulation, transactions
from multiversx_sdk_network_providers import errors, proxy_network_provider
from rich import print
from rich.pretty import pprint

from scribe import constants as sc_constants
from scribe import settings

from . import info, loader, output


def deploy_contract(
    contract_cargo: info.SmartContractData,
    account: accounts.Account,
    env: sc_constants.EnvironmentType,
) -> output.DeploymentResult:
    """Deploys a contract on the blockchain using configuration from scdeploy.yaml

    :param contract_cargo: Content of the contract Cargo.toml
    :param account: Account to use for deployment
    :param env: Environment to deploy to
    """
    deploy_config = loader.load_deploy_config(contract_cargo.contract_path, env)
    contract_deploy_config = deploy_config.get(env.value, {}).get(contract_cargo.name, {})

    bytecode = loader.load_bytecode(contract_cargo)
    metadata = contracts.CodeMetadata(**contract_deploy_config.get("code_metadata", {}))
    proxy = proxy_network_provider.ProxyNetworkProvider(settings.PROXY)
    sc = contracts.SmartContract(bytecode=bytecode, metadata=metadata)

    print(f"{settings.LOGGING_INFO_PREFIX} Deploying contract: [[green bold] {contract_cargo.name} [/]]")
    print(f"{settings.LOGGING_INFO_PREFIX} - Owner address:    [[cyan bold] {account.address} [/]]")
    typer.confirm("\nConfirm deployment: ", abort=True)
    tx = sc.deploy(
        owner=account,
        arguments=contract_deploy_config.get("args", []),
        gas_price=contract_deploy_config.get("gasPrice", settings.DEFAULT_GAS_PRICE),
        gas_limit=contract_deploy_config.get("gasLimit", 0),
        value=contract_deploy_config.get("value", 0),
        chain=settings.CHAIN_ID,
        version=settings.TX_VERSION,
    )
    print(f"{settings.LOGGING_INFO_PREFIX} - Contract address: [[cyan bold] {sc.address} [/]]")

    deployment_status = send_or_simulate_simple(tx, proxy, simulate=False)

    return output.DeploymentResult(
        status=deployment_status,
        env=env,
        contract_data=contract_cargo,
        contract_address=sc.address if deployment_status == output.DeploymentStatus.SUCCESS else None,
        tx_hash=tx.hash,
    )


def upgrade_contract(
    contract_cargo: info.SmartContractData,
    account: accounts.Account,
    env: sc_constants.EnvironmentType,
) -> None:
    """Upgrades a contract on the blockchain using configuration from scdeploy.yaml

    :param contract_cargo: Content of the contract Cargo.toml
    :param account: Account to use for deployment
    :param env: Environment to deploy to
    """
    deploy_config = loader.load_deploy_config(contract_cargo.contract_path, env)
    contract_deploy_config = deploy_config.get(env.value, {}).get(contract_cargo.name, {})
    bytecode = loader.load_bytecode(contract_cargo)
    metadata = contracts.CodeMetadata(**contract_deploy_config.get("code_metadata", {}))
    proxy = proxy_network_provider.ProxyNetworkProvider(settings.PROXY)
    sc = contracts.SmartContract(bytecode=bytecode, metadata=metadata)

    if settings.DEFAULT_CONFIG_SC_ADDRESS_FIELD not in contract_deploy_config:
        raise Exception(f"Missing field {settings.DEFAULT_CONFIG_SC_ADDRESS_FIELD} in scdeploy.yaml")

    sc.address = accounts.Address(contract_deploy_config.get(settings.DEFAULT_CONFIG_SC_ADDRESS_FIELD))
    typer.confirm("\nConfirm upgrade: ", abort=True)
    tx = sc.upgrade(
        owner=account,
        arguments=contract_deploy_config.get("args", []),
        gas_price=contract_deploy_config.get("gasPrice", settings.DEFAULT_GAS_PRICE),
        gas_limit=contract_deploy_config.get("gasLimit", 0),
        value=contract_deploy_config.get("value", 0),
        chain=settings.CHAIN_ID,
        version=settings.TX_VERSION,
    )

    send_or_simulate_simple(tx, proxy, simulate=False)

    return None


def send_or_simulate_simple(
    tx: transactions.Transaction,
    proxy: proxy_network_provider.ProxyNetworkProvider,
    simulate: bool = True,
) -> output.DeploymentStatus:
    try:
        if simulate:
            sim = simulation.Simulator(proxy).run(tx)
            print(f"{settings.LOGGING_INFO_PREFIX} Tx Sim Completed")
            pprint(sim.simulation_response.__dict__)
        else:
            tx_on_network = tx.send_wait_result(proxy, settings.TIMEOUT)
            print(f"{settings.LOGGING_INFO_PREFIX} Tx Sent")

            tx_output = tx_on_network.to_dictionary()
            output_data = {
                "txHash": tx_output.get("hash", {}),
                "completed": tx_on_network.is_completed,
                "nonce": tx_output.get("nonce", {}),
                "sender": tx_output.get("sender", {}),
                "receiver": tx_output.get("receiver", {}),
            }

            pprint(output_data, expand_all=True)

        return output.DeploymentStatus.SUCCESS
    except errors.GenericError as ex:
        print(f"[ [red bold]ERROR[/] ] [yellow]{ex.data.get('error', {})}[/]")
        return output.DeploymentStatus.FAIL
