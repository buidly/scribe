import pytest

from pathlib import Path
from scribe import wallet
from multiversx_sdk_cli import accounts

from pytest_mock import MockerFixture


def test_build_account_from_pem(test_pem_file: Path, mocker: MockerFixture):

    def sync_nonce_mock(self, proxy):
        self.nonce = 32

    mocker.patch.object(accounts.Account, "sync_nonce", sync_nonce_mock)
    res_account = wallet.build_account_from_pem(test_pem_file)

    assert res_account.nonce == 32
    assert res_account.address is not None


def test_build_account_from_pem_raise(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        wallet.build_account_from_pem(tmp_path / "test.pem")


def test_build_account_from_pem_corrupted(test_pem_file_corrupted: Path):
    with pytest.raises(UnicodeDecodeError):
        wallet.build_account_from_pem(test_pem_file_corrupted)
