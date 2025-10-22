"""Command line interface for FakeHippoRag."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import AppConfig, ConfigurationError, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FakeHippoRag pipeline controller")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a TOML configuration file. Defaults to config/default.toml.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="Hello, world!",
        help="Sample query to run through the pipeline.",
    )
    return parser


def _mock_retriever(_: AppConfig):  # pragma: no cover - trivial wiring
    from . import retrievers  # noqa: F401  # Import to demonstrate package structure

    class DefaultRetriever:
        def retrieve(self, query: str) -> list[str]:
            return [f"Retrieved context for: {query}"]

    return DefaultRetriever()


def _mock_generator(_: AppConfig):  # pragma: no cover - trivial wiring
    from . import generators  # noqa: F401  # Import to demonstrate package structure

    class DefaultGenerator:
        def generate(self, query: str, context: list[str]) -> str:
            contexts = " | ".join(context) if context else "<empty>"
            return f"Generated response for '{query}' with context: {contexts}"

    return DefaultGenerator()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except ConfigurationError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover

    retriever = _mock_retriever(config)
    generator = _mock_generator(config)

    contexts = retriever.retrieve(args.query)
    response = generator.generate(args.query, contexts)

    print(f"Project: {config.project_name} v{config.version}")
    print(f"Retriever: {config.retriever_backend}")
    print(f"Generator: {config.generator_backend}")
    print("---")
    print(response)

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
