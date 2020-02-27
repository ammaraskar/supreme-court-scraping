import pytest
from sc_scraper import case_code


def test_invalid_case_code():
    with pytest.raises(ValueError):
        case_code.parse_case_code("totally wrong")


def test_invalid_jurisdiction():
    with pytest.raises(ValueError):
        case_code.parse_case_code("NSH")


def test_invalid_court():
    with pytest.raises(ValueError):
        case_code.parse_case_code("CXY")


def test_invalid_nature():
    with pytest.raises(ValueError):
        case_code.parse_case_code("CTA")


def test_valentino_v_new_york():
    parsed = case_code.parse_case_code("CSY")

    assert parsed.jurisdiction == case_code.JurisdictionalGrounds.Certiorari
    assert parsed.court_below == case_code.CourtBelow.State
    assert parsed.nature == case_code.Nature.Criminal
