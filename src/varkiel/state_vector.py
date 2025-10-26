# SPDX-License-Identifier: MPL-2.0
"""Unified state vector representation used across the Varkiel system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class StateVector:
    """Container for both symbolic text and numerical state encodings."""

    text: Optional[str] = None
    embeddings: np.ndarray = field(default_factory=lambda: np.array([], dtype=float))
    state: np.ndarray = field(default_factory=lambda: np.array([], dtype=float))
    original_embeddings: np.ndarray = field(default_factory=lambda: np.array([], dtype=float))
    coherence_score: float = 0.0
    coherence_level: float = 0.0
    metrics: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    audit_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def coherence(self) -> float:
        """Compatibility shim for legacy code using the `coherence` attribute."""
        return self.coherence_level if self.coherence_level else self.coherence_score

    @coherence.setter
    def coherence(self, value: float) -> None:
        self.coherence_level = value
        self.coherence_score = value

    @classmethod
    def from_input(cls, text: str) -> "StateVector":
        """Create a state vector from raw text input."""
        return cls(text=text, metrics={"input_length": float(len(text))})

    def add_metric(self, name: str, value: float) -> None:
        """Add or update a processing metric."""
        self.metrics[name] = value

    def add_warning(self, message: str) -> None:
        """Record a processing warning."""
        self.warnings.append(message)

    def add_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Append an audit trail event."""
        events = self.audit_data.setdefault("events", [])
        events.append({
            "type": event_type,
            "timestamp": self.timestamp,
            "data": data,
        })

    def update_state(self, state: np.ndarray, coherence: float) -> None:
        """Synchronise the numerical state representation and coherence metrics."""
        self.state = np.asarray(state, dtype=float)
        self.coherence_level = coherence
        self.coherence_score = coherence
        self.metrics["coherence_score"] = coherence

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the state vector to a JSON-serialisable dictionary."""
        return {
            "text": self.text,
            "embeddings": self.embeddings.tolist() if self.embeddings.size else [],
            "state": self.state.tolist() if self.state.size else [],
            "original_embeddings": self.original_embeddings.tolist() if self.original_embeddings.size else [],
            "coherence_score": self.coherence_score,
            "coherence_level": self.coherence_level,
            "metrics": self.metrics,
            "warnings": self.warnings,
            "audit_data": self.audit_data,
            "timestamp": self.timestamp,
        }
