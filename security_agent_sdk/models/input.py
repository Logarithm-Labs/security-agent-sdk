from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")
    address: str
    chain_id: int


class RequirementScheme(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contracts: List[Contract]
    github_repo_url: HttpUrl
