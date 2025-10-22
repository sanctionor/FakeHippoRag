"""Configuration loading utilities for the FakeHippoRag project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:  # pragma: no cover - import guard depends on Python version
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    import tomli as tomllib  # type: ignore[import-not-found]


DEFAULT_CONFIG_PATH = Path("config/default.toml")


@dataclass(frozen=True)
class AppConfig:
    """Top-level application configuration."""

    project_name: str
    version: str
    retriever_backend: str
    generator_backend: str


class ConfigurationError(RuntimeError):
    """Raised when a configuration file cannot be loaded or parsed."""


def load_config(path: Path | str | None = None) -> AppConfig:
    """Load application configuration from the given TOML file.

    Args:
        path: Optional path to a TOML configuration file. When not provided,
            :data:`DEFAULT_CONFIG_PATH` is used.

    Returns:
        An :class:`AppConfig` instance with the parsed configuration.

    Raises:
        ConfigurationError: If the file cannot be read or the content is invalid.
    """

    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH

    if not config_path.exists():
        message = f"Configuration file not found: {config_path}"
        raise ConfigurationError(message)

    try:
        with config_path.open("rb") as handle:
            raw_config = tomllib.load(handle)
    except OSError as exc:  # pragma: no cover - critical failure
        raise ConfigurationError(str(exc)) from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigurationError(str(exc)) from exc

    app_section = _expect_section(raw_config, "app")

    try:
        return AppConfig(
            project_name=_expect_str(app_section, "project_name"),
            version=_expect_str(app_section, "version"),
            retriever_backend=_expect_str(app_section, "retriever_backend"),
            generator_backend=_expect_str(app_section, "generator_backend"),
        )
    except KeyError as exc:
        raise ConfigurationError(f"Missing configuration key: {exc}") from exc


def _expect_section(config: dict[str, Any], key: str) -> dict[str, Any]:
    section = config.get(key)
    if not isinstance(section, dict):
        raise ConfigurationError(f"Section '{key}' is missing or invalid.")
    return section


def _expect_str(section: dict[str, Any], key: str) -> str:
    value = section[key]
    if not isinstance(value, str):
        raise ConfigurationError(f"Configuration value '{key}' must be a string.")
    return value
