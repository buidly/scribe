from scribe import exceptions


class WorkspaceNotFound(exceptions.BaseException):
    """This path is not a smart contracts workspace"""

    pass


class ContractCargoNotFound(exceptions.BaseException):
    """Contract Cargo.toml file not found"""

    pass


class ContractCargoInvalid(exceptions.BaseException):
    """Cargo.toml file is invalid"""

    pass


class ContractNotFound(exceptions.BaseException):
    """Contract not found in workspace"""

    pass


class MissingInteractionsFolder(exceptions.BaseException):
    """Interactions folder not found"""

    pass


class MissingDevNetInteractionsFile(exceptions.BaseException):
    """Devnet interactions file not found"""

    pass


class MissingDeployConfigFile(exceptions.BaseException):
    """Deploy config file not found"""

    pass


class MissingBytecodeFile(exceptions.BaseException):
    """Bytecode file not found"""

    pass


class CouldNotLoadBytecode(exceptions.BaseException):
    """Could not load bytecode from file"""

    pass
