from typing import List

from pydantic import BaseModel, HttpUrl
from pydantic import ConfigDict


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: str
    chain: int


class Vault(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vault_address: str
    chain: int


class RequirementScheme(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vault: Vault
    contracts: List[Contract]
    github_repo_url: HttpUrl


