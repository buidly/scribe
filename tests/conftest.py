import pytest
import pathlib


@pytest.fixture
def test_pem_file(tmp_path: pathlib.Path) -> pathlib.Path:
    f = tmp_path / "test.pem"
    f.write_text("""
-----BEGIN PRIVATE KEY for erd19m5vyshr2rn4dmjju7gwpqa9jyl4lwp45awuctpmrk2tq2657pyqwxcm2z-----
NTMyMzJkZjVhYzEyYTgxYmM3ZTZlYWY5MDRkOGE1OGNmMDVjZjM2MWNhZTY0ZTgy
MGQxZjIzNzdlN2ZjN2ZiZjJlZThjMjQyZTM1MGU3NTZlZTUyZTc5MGUwODNhNTkx
M2Y1ZmI4MzVhNzVkY2MyYzNiMWQ5NGIwMmI1NGYwNDg=
-----END PRIVATE KEY for erd19m5vyshr2rn4dmjju7gwpqa9jyl4lwp45awuctpmrk2tq2657pyqwxcm2z-----
    """)

    return f


@pytest.fixture
def test_pem_file_corrupted(tmp_path: pathlib.Path) -> pathlib.Path:
    f = tmp_path / "test.pem"
    f.write_text("""
-----BEGIN PRIVATE KEY for erd19m5vyshr2rn4dmjju7gwpqa9jyl4lwp45awuctpmrk2tq2657pyqwxcm2z-----
NTMyMzJkZjVhYzEyYTgxYmM3ZTZlYWY5MDRkOGE1OGNmMDVjZjM2MWNhZTY0ZTgy
MGQxZjIzNzdlN2ZjN2ZiZjJlZThjMjQyZTM1MGU3NTZlZTUyZTc5MGUwODNhNasf
M2Y1ZmI4MzVhNzVkY2MyYzNiMWQ5NGIwMmI1NGYwNDg=
-----END PRIVATE KEY for erd19m5vyshr2rn4dmjju7gwpqa9jyl4lwp45awuctpmrk2tq2657pyqwxcm2z-----
    """)

    return f
