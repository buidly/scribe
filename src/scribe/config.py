from pathlib import Path


class Config:
    """Default configuration for CLI"""

    ENVIRONMENT: str = ""
    WORKSPACE_FILE_NAME: list[str] = [
        "multiversx.workspace.json",
        "elrond.workspace.json",
    ]
    CONTRACT_ROOT_FILE: list[str] = [
        "multiversx.json",
        "elrond.json"
    ]
    RUST_CARGO_FILE: str = "Cargo.toml"
    INTERACTIONS_DIR_NAME: str = "interactions"
    INTERACTIONS_FILE_NAME: str = "snippets.sh"
    OUTPUT_DIR_NAME: str = "output"
    DEPLOY_CONFIG_NAME: str = "scdeploy.yaml"
    PROXY: str = ""
    VM_TYPE_WASM_VM: str = "0500"
    VM_TYPE_SYSTEM = "0001"
    BYTECODE_TYPE: str = "wasm"
    CHAIN_ID: str = ""
    TX_VERSION: int = 1
    TIMEOUT: int = 100
    LOGGING_INFO_PREFIX: str = "[[green bold] INFO [/]]"
    DEFAULT_GAS_PRICE: int = 1000000000
    MX_SDK_DIR_PATH: Path = Path("~").expanduser() / "multiversx-sdk"
    TEST_WALLETS_PATH: Path = (MX_SDK_DIR_PATH / "testwallets" / "v1.0.0" / "elrond-sdk-testwallets-1.0.0" / "users")
    DEFAULT_TEST_WALLET: Path = TEST_WALLETS_PATH / "alice.pem"
    TMP_PATH_FOR_WALLET: Path = Path(".") / "tmp"
    DEFAULT_REPO_WALLET_FILE_NAME: str = "default.pem"
    DEFAULT_BUIDL_DIR: Path = Path("~").expanduser() / ".buidl"
    DEFAULT_BUIDL_CONFIG_FILE: Path = DEFAULT_BUIDL_DIR / "config.yaml"
    DEFAULT_CONFIG_SC_ADDRESS_FIELD: str = "sc_address"
    EXPLORER_ACCOUNT_TEMPLATE: str = "https://{env}-explorer.multiversx.com/accounts/{address}"
    EXPLORER_TX_TEMPLATE: str = "https://{env}-explorer.multiversx.com/transactions/{tx_hash}"

    def load_devnet(self):
        """Load devnet configuration"""
        self.ENVIRONMENT = "devnet"
        self.PROXY = "https://devnet-gateway.multiversx.com"
        self.CHAIN_ID = "D"

    def load_testnet(self):
        """Load testnet configuration"""
        self.ENVIRONMENT = "testnet"
        self.PROXY = "https://testnet-gateway.multiversx.com"
        self.CHAIN_ID = "T"

    def load_test_config(self, tmp_path: Path):
        """Load test configuration"""
        self.ENVIRONMENT = "test"
        self.PROXY = "https://test.com"
        self.CHAIN_ID = "T"
        self.MX_SDK_DIR_PATH = tmp_path / "multiversx-sdk"
