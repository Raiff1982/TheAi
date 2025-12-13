"""
[DEPRECATED] Web Interface for Codette
This file is deprecated. Please use the unified interface at /codette_interface.py instead.

Example usage:
    from codette_interface import create_interface
    app = create_interface("web")
    app.run()
"""

import warnings
warnings.warn(
    "This interface is deprecated. Please use the unified interface at /codette_interface.py instead.",
    DeprecationWarning,
    stacklevel=2
)

from codette_interface import create_interface

# Provide backwards compatibility
def create_web_app():
    """Backwards compatibility wrapper"""
    warnings.warn(
        "Use create_interface('web') instead of create_web_app()",
        DeprecationWarning,
        stacklevel=2
    )
    return create_interface("web")