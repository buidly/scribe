import github
import github.Repository
import yaml

from . import exceptions, settings


def _import_user_config() -> dict[str, str]:
    """Imports user config from .buidl directory"""

    if not settings.DEFAULT_BUIDL_DIR.exists() or not settings.DEFAULT_BUIDL_CONFIG_FILE.exists():
        raise exceptions.UserConfigNotFound()

    with open(settings.DEFAULT_BUIDL_CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def init_github() -> github.Github:
    """Initializes github client"""

    user_config = _import_user_config()
    access_token = user_config.get("gh-token", "")

    return github.Github(access_token)


def get_repository(client: github.Github, repo_name: str) -> github.Repository.Repository:
    """Fetches a repository from github"""

    try:
        return client.get_repo(repo_name)
    except github.UnknownObjectException as ex:
        print(ex)
        raise exceptions.RepositoryNotFound()
