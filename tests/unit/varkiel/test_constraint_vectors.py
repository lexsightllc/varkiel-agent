# SPDX-License-Identifier: MPL-2.0
"""Unit tests for constraint lattice adapter vector operations."""

from __future__ import annotations

import numpy as np
import pytest
from unittest.mock import patch

from varkiel.constraint_lattice_adapter import ConstraintLatticeAdapter
from varkiel.structural_constraint_engine import ConstraintType


@pytest.fixture()
def adapter() -> ConstraintLatticeAdapter:
    """Create an adapter with deterministic defaults for testing."""
    np.random.seed(0)
    return ConstraintLatticeAdapter()


def test_suspension_vector_no_paradox(adapter: ConstraintLatticeAdapter) -> None:
    """Suspension returns the original state when no paradox is detected."""
    state = np.array([0.5, 0.5, 0.5], dtype=float)
    result = adapter._apply_suspension(state)
    np.testing.assert_allclose(result.state, state)


def test_suspension_vector_with_paradox(adapter: ConstraintLatticeAdapter) -> None:
    """Suspension zeros the state when paradox detection triggers."""
    state = np.array([0.5, 0.5, 0.5], dtype=float)
    with patch.object(adapter, "_is_high_stakes_paradox", return_value=True):
        result = adapter._apply_suspension(state)
    np.testing.assert_allclose(result.state, np.zeros_like(state))
    assert result.coherence_level == pytest.approx(0.0)


def test_overalignment_vector(adapter: ConstraintLatticeAdapter) -> None:
    """Overalignment scales the state by the security consensus factor."""
    adapter.security_consensus_factor = 0.8
    state = np.ones(3, dtype=float)
    result = adapter._apply_overalignment(state)
    np.testing.assert_allclose(result.state, state * 0.8)


def test_causal_erasure_vector(adapter: ConstraintLatticeAdapter) -> None:
    """Causal erasure replaces the state with a generalized representation."""
    state = np.array([0.1, 0.5, 0.9], dtype=float)
    with patch.object(adapter, "_generalize_state", return_value=np.full_like(state, 0.5)):
        result = adapter._apply_causal_erasure(state)
    np.testing.assert_allclose(result.state, np.full_like(state, 0.5))


def test_apply_constraint_vector_dispatch(adapter: ConstraintLatticeAdapter) -> None:
    """apply_constraint_vector delegates to the correct strategy."""
    state = np.ones(3, dtype=float)
    with patch.object(adapter, "_apply_suspension") as suspension_spy:
        adapter.apply_constraint_vector(state, ConstraintType.SUSPENSION)
    suspension_spy.assert_called_once_with(state)
