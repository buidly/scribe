import functools
from typing import Any, Callable

from rich import print


class BaseException(Exception):
    ui_message: str | None = None

    def __init__(self, *args: object):
        self.ui_message = self.__doc__
        super().__init__(*args)


def exptr(func: Callable[..., Any], *args, **kwargs):
    """A fail check decorator that can handle all Base Exceptions from
    within the CLI.

    All Base Exceptions should have a ui_message attribute that is derived
    from the __docs__ attribute of the class, and will be printed to the
    user.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable[..., Any] | None:
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print(f"[[red bold] ERR [/]] [yellow] {e.ui_message} [/]")
            return None
        except Exception:
            raise

    return wrapper


class IncorrectPemWiseArguments(BaseException):
    """Incorrect pem wise arguments"""
    pass


class RepositoryNotFound(BaseException):
    """Repository not found at path"""
    pass


class MxSdkNotFound(BaseException):
    """MultiversX SDK not found at path"""
    pass


class UserConfigNotFound(BaseException):
    """Cannot find default user configuration in root"""
    pass


class PemFileForEnvNotFound(BaseException):
    """Cannot find pem file for environment in repository"""
    pass


class ContractDeployConfigNotFound(BaseException):
    """Cannot find contract deploy configuration for this environment"""
    pass
