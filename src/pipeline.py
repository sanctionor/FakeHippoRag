"""Core pipeline abstractions for the FakeHippoRag project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .config import AppConfig


class Retriever(Protocol):
    """Protocol representing a retrieval component."""

    def retrieve(self, query: str) -> list[str]:
        """Retrieve context documents for the given query."""


class Generator(Protocol):
    """Protocol representing a generation component."""

    def generate(self, query: str, context: list[str]) -> str:
        """Generate a response for the given query and context."""


@dataclass
class Pipeline:
    """Simple Retrieval-Augmented Generation pipeline."""

    config: AppConfig
    retriever: Retriever
    generator: Generator

    def run(self, query: str) -> str:
        """Execute the pipeline for the given query."""

        context = self.retriever.retrieve(query)
        return self.generator.generate(query, context)
