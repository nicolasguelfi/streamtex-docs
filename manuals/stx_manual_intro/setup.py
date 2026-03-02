"""StreamTeX project setup — configures import paths."""
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
MANUALS_DIR = PROJECT_DIR.parent

# Shared blocks for cross-manual imports
SHARED_BLOCKS_DIR = MANUALS_DIR / "shared-blocks"
if SHARED_BLOCKS_DIR.exists() and str(SHARED_BLOCKS_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_BLOCKS_DIR))
