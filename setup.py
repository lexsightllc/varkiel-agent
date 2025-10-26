# SPDX-License-Identifier: MPL-2.0
"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

from setuptools import setup, find_packages

setup(
    name="varkiel",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="MPL-2.0",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "requests>=2.26.0",
        "tenacity>=8.0.0",
        "pydantic>=1.9.0",
        "sentence-transformers>=2.2.0",
        "flask>=2.3.0",
        "flask-login>=0.6.0",
        "prometheus-client>=0.20.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.8.0",
        "torch>=2.1.0",
        "gunicorn>=21.2.0",
    ],
)
