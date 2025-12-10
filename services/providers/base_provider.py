from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLeadProvider(ABC):
    """
    Abstract Interface for Lead Data Providers.
    All data sources (Mock, Apollo, Hunter, etc.) must implement this.
    """

    @abstractmethod
    def fetch_leads(self, industry: str, location: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Fetches raw lead data.
        Returns a list of dictionaries with keys:
        company_name, contact_name, email, phone, score (optional)
        """
        pass
