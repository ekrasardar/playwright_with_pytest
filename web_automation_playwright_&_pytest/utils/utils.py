from enum import Enum


class Env(Enum):
    PROD = "prod"
    PREPROD = "preprod"
    STAGING = "staging"
    SANDBOX = "sandbox"

class Lang(Enum):
    EN = "en"
    TH = "th"
    MY = "mm"
    KM = "kh"
