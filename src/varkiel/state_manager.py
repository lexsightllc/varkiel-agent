"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

"""
Varkiel Agent - Advanced AI Constraint System
Copyright (C) 2025 Lexsight LLC
SPDX-License-Identifier: AGPL-3.0-only OR Commercial
"""

import json
import os
from pathlib import Path

import numpy as np

class StateManager:
    def __init__(self, storage_path: str | os.PathLike[str] | None = None):
        default_path = Path(__file__).resolve().parents[2] / "data" / "state.json"
        self.storage_path = Path(storage_path) if storage_path else default_path
        self.episodic_memory = []
        self.load_state()
        
    def record_episode(self, input_text, output_vector, symbolic_interpretation):
        self.episodic_memory.append({
            'input': input_text,
            'output': output_vector.tolist(),
            'symbols': symbolic_interpretation
        })
        self.save_state()
        
    def save_state(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open('w', encoding='utf-8') as f:
            json.dump(self.episodic_memory, f)

    def load_state(self):
        if self.storage_path.exists():
            with self.storage_path.open('r', encoding='utf-8') as f:
                self.episodic_memory = json.load(f)
