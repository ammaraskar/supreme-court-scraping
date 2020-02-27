import collections
from enum import Enum


CaseCode = collections.namedtuple("CaseCode", ["jurisdiction", "court_below", "nature"])


class JurisdictionalGrounds(Enum):
    Certiorari = "C"
    Appeal = "A"
    CertifiedQuestion = "Q"


class CourtBelow(Enum):
    State = "S"
    USCourtOfAppeals = "F"
    ThreeJudgeDistrict = "T"
    AppealsForArmedForces = "M"
    Other = "O"


class Nature(Enum):
    Civil = "X"
    Criminal = "Y"
    HabeasCorpus = "H"


def parse_case_code(code):
    if len(code) != 3:
        raise ValueError("Case codes are 3 characters long")

    jurisdiction = JurisdictionalGrounds(code[0])
    court_below = CourtBelow(code[1])
    nature = Nature(code[2])

    return CaseCode(jurisdiction, court_below, nature)
