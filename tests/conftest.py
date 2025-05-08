# tests/conftest.py
import os
import sys

# repo root
ROOT = os.path.dirname(os.path.dirname(__file__))

# allow `import ssh_server`
sys.path.insert(0, ROOT)

# allow `import vm_core`
sys.path.insert(0, os.path.join(ROOT, "vm_core", "src"))
