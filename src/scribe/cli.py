from pathlib import Path

import typer
import pygit2
from rich import print

from scribe.constants import EnvironmentType

from . import exceptions, wallet
from .contracts import deploy, loader
from .deployment import tag

app = typer.Typer()


@app.callback()
def callback():
    """MX Smart Contracts CLI for deployment and management"""
    pass


@app.command(help="Deploys a contract from workspace", name="deploy")
@exceptions.exptr
def deploy_contract(
    env: EnvironmentType = typer.Argument(..., help="Environment to deploy to"),
    contract_name: str = typer.Argument(...),
    pem_file: str = typer.Option(default=None),
    pem_repo: str = typer.Option(default=None),
) -> None:
    env.load_config()
    loaded_path = Path(".")
    if pem_repo and not pem_file:
        account = wallet.build_account_from_repo(pem_repo, env)
    elif pem_file and not pem_repo:
        account = wallet.build_account_from_pem(Path(pem_file))
    elif not pem_file and not pem_repo:
        account = wallet.build_account_default()
    else:
        raise exceptions.IncorrectPemWiseArguments()

    workspace = loader.load_workspace(loaded_path)
    contract = workspace.get(contract_name)
    deployment_result = deploy.deploy_contract(contract, account, env)
    deployment_result.resolve()


@app.command(help="Upgrades a contract from workspace", name="upgrade")
@exceptions.exptr
def upgrade_contract(
    env: EnvironmentType = typer.Argument(..., help="Environment to deploy to"),
    contract_name: str = typer.Argument(...),
    pem_file: str = typer.Option(default=None),
    pem_repo: str = typer.Option(default=None),
) -> None:
    env.load_config()
    loaded_path = Path(".")
    if pem_repo and not pem_file:
        account = wallet.build_account_from_repo(pem_repo, env)
    elif pem_file and not pem_repo:
        account = wallet.build_account_from_pem(Path(pem_file))
    elif not pem_file and not pem_repo:
        account = wallet.build_account_default()
    else:
        raise exceptions.IncorrectPemWiseArguments()

    workspace = loader.load_workspace(loaded_path)
    contract = workspace.get(contract_name)
    deploy.upgrade_contract(contract, account, env)


@app.command(help="Display all contracts from workspace")
@exceptions.exptr
def get_contracts() -> None:
    """Fetches all contracts names from workspace"""
    loaded_path = Path(".")
    workspace = loader.load_workspace(loaded_path)
    print("[ Workspace contracts ]")
    for contract in workspace.contracts:
        print(f"[green bold]:: {contract.name}[/]")


@app.command(help="Display all tags from repo")
@exceptions.exptr
def get_tags() -> None:
    """Fetches all tags from github repo"""
    local_repo = pygit2.Repository(".")
    print("[ Tags ]")
    for t in tag.get_tags_references(local_repo):
        print(f"[green bold]:: {t.removeprefix('refs/tags/')}[/]")


@app.command(help="Deploy contract from tag")
@exceptions.exptr
def deploy_tag(
    tag_name: str = typer.Argument(...),
    env: EnvironmentType = typer.Argument(..., help="Environment to deploy to"),
    contract_name: str = typer.Argument(...),
    pem_file: str = typer.Option(default=None),
    pem_repo: str = typer.Option(default=None),
) -> None:
    local_repo = pygit2.Repository(".")
    current_branch = tag.get_current_branch(local_repo)
    tag.checkout_tag_branch(local_repo, tag_name)
    deploy_contract(env, contract_name, pem_file, pem_repo)
    tag.checkout_branch(local_repo, current_branch)
