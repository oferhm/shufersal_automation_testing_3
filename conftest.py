# conftest.py  (root)
# ──────────────────────────────────────────────────────────────────────────────
# conftest.py — Pytest's auto-loaded plugin file.
#
# WHY THIS FILE EXISTS:
#   Pytest automatically discovers and loads conftest.py at startup.
#   Any fixture imported (or defined) here becomes available to ALL test
#   files without a single import statement in the test files themselves.
#
# PATTERN: Define fixtures in focused files (fixtures/), register them here.
# ──────────────────────────────────────────────────────────────────────────────

from fixtures.browser_fixtures import (  # noqa: F401
    browser_instance,
    context,
    page,
    home_page,
)