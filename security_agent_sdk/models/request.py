from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from yield_analysis_sdk.type import Chain
from yield_analysis_sdk.validators import ChainMixin

from ..validation import AddressValidatorMixin


class Contract(AddressValidatorMixin, ChainMixin, BaseModel):
    address: str
    chain: Chain


class RegistrationRequest(BaseModel):
    """Registration request with vault contract and additional contracts list."""

    vault: Contract
    contracts: Optional[List[Contract]] = None
    github_repo_url: Optional[HttpUrl] = None
