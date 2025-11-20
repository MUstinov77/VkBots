from enum import Enum


class BotDomain(Enum):
    canary = "canary"
    regular = "regular"


class BotEnv(Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"