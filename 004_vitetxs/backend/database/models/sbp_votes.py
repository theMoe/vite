from pydantic.main import BaseModel

class SBPVotes(BaseModel):
    sbp_name: str
    block_producing_address: str
    votes: str
    count: int
    ratio: float
    block_creation_rewards: float
    rewards_of_votes: float
    rewards_in_total: float

    class Config:
        orm_mode = True