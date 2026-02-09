"""Constitution service for app configuration management."""

from typing import Any, Dict


class ConstitutionService:
    """Service managing app configuration in memory.

    Configuration is stored in-memory and lost when application exits.

    Attributes:
        _config: Dictionary holding app configuration
    """

    def __init__(self, initial_config: Dict[str, Any] | None = None) -> None:
        """Initialize ConstitutionService with optional initial config.

        Args:
            initial_config: Optional dictionary of initial configuration values
        """
        self._config: Dict[str, Any] = initial_config.copy() if initial_config else {}

    def update(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update app configuration with given updates.

        Merges the updates into existing configuration.

        Args:
            updates: Dictionary of configuration updates

        Returns:
            Updated configuration dictionary
        """
        self._config.update(updates)
        return self._config.copy()

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration.

        Returns:
            Copy of current configuration dictionary
        """
        return self._config.copy()
