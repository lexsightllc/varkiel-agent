"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class AuditLogger:
    def __init__(self, config: Dict[str, Any]):
        default_key = Path(__file__).resolve().parents[2] / "infra" / "certs" / "private_key.pem"
        configured_key = config.get('private_key_path') or os.getenv('VARKIEL_PRIVATE_KEY_PATH')
        self.log_file = config.get('log_file', 'audit.log')
        self.private_key_path = Path(configured_key) if configured_key else default_key
        self.log_format = config.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Initialize logger
        self.logger = logging.getLogger('audit_logger')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(self.log_format)
        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)
        self.log: List[Dict[str, Any]] = []

    def log_decision(self, prompt: str, response: str, context: dict) -> str:
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'prompt': prompt,
            'response': response,
            'context': context
        }
        entry_str = json.dumps(entry, sort_keys=True)
        entry_id = hashlib.sha256(entry_str.encode()).hexdigest()
        
        with open(self.private_key_path, 'rb') as key_file:
            private_key = load_pem_private_key(
                key_file.read(),
                password=None
            )
        signature = private_key.sign(
            entry_str.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        self.log.append({
            'id': entry_id,
            'entry': entry,
            'signature': signature.hex()
        })
        return entry_id

    def log_error(self, error: Exception, context: dict) -> None:
        """Log an error during processing"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(error),
            'context': context
        }
        self.logger.error(json.dumps(entry))

    def log_error(self, error: Exception, context: dict) -> None:
        """Log an error during processing"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(error),
            'context': context
        }
        self.logger.error(entry)
