from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Dict


@dataclass
class POI:
    name: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    opening_hours: Optional[dict] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add or update a metadata field."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata field value."""
        return self.metadata.get(key, default)

    def remove_metadata(self, key: str) -> None:
        """Remove a metadata field."""
        self.metadata.pop(key, None)

    def has_metadata(self, key: str) -> bool:
        """Check if a metadata field exists."""
        return key in self.metadata


@dataclass
class TripPoint:
    poi: POI
    visit_date: datetime
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add or update a metadata field."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata field value."""
        return self.metadata.get(key, default)

    def remove_metadata(self, key: str) -> None:
        """Remove a metadata field."""
        self.metadata.pop(key, None)

    def has_metadata(self, key: str) -> bool:
        """Check if a metadata field exists."""
        return key in self.metadata
