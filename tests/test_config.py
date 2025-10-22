from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import ConfigurationError, load_config


def test_load_default_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        """
        [app]
        project_name = "Test"
        version = "1.0"
        retriever_backend = "mock"
        generator_backend = "mock"
        """
    )

    config = load_config(config_file)

    assert config.project_name == "Test"
    assert config.version == "1.0"
    assert config.retriever_backend == "mock"
    assert config.generator_backend == "mock"


def test_missing_config_file() -> None:
    with pytest.raises(ConfigurationError):
        load_config(Path("does-not-exist.toml"))
