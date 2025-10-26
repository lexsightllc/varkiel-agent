# SPDX-License-Identifier: MPL-2.0
"""Unit tests for the `StateVector` data structure."""

from __future__ import annotations

import numpy as np

from varkiel.state_vector import StateVector


def test_update_state_sets_metrics() -> None:
    state = StateVector.from_input("hello world")
    vector = np.array([0.1, 0.2, 0.3], dtype=float)

    state.update_state(vector, coherence=0.75)

    np.testing.assert_array_equal(state.state, vector)
    assert state.coherence_level == 0.75
    assert state.metrics["coherence_score"] == 0.75


def test_add_audit_event_appends_event() -> None:
    state = StateVector.from_input("eventful")
    state.add_audit_event("test", {"value": 1})

    assert "events" in state.audit_data
    assert state.audit_data["events"][0]["type"] == "test"
