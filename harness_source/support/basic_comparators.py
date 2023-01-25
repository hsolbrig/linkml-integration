from typing import Optional

from harness_source.support.compare_rdf import compare_rdf


def string_comparator(expected: str, actual: str) -> Optional[str]:
    """
    Compare two strings w/ embedded line feeds.  Return a simple match/nomatch output message
    :param expected: expected string
    :param actual: actual string
    :return: Error message if mismatch else None
    """
    if expected.replace("\r\n", "\n").strip() != actual.replace("\r\n", "\n").strip():
        return f"Output changed."


def jsonld_comparator(expected_data: str, actual_data: str) -> str:
    """Compare expected data in json-ld format to actual data in json-ld format"""
    return compare_rdf(expected_data, actual_data, "json-ld")


def n3_comparator(expected_data: str, actual_data: str) -> str:
    """compare expected_data in n3 format to actual_data in n3 format"""
    return compare_rdf(expected_data, actual_data, "n3")


def rdf_comparator(
    expected_data: str, actual_data: str, fmt: Optional[str] = "turtle"
) -> str:
    """compare expected_data to actual_data using basic RDF comparator method"""
    return compare_rdf(expected_data, actual_data, fmt=fmt)


def always_pass_comparator(
    expected_data: str, new_data: str
) -> Optional[str]:
    """
    No-op comparator -- everyone passes!
    :param expected_data:
    :param new_data:
    :return:
    """
    return None


def closein_comparison(expected_txt: str, actual_txt: str) -> None:
    """Assist with testing comparison -- zero in on the first difference in a big string

    @param expected_txt:
    @param actual_txt:
    """
    window = 30
    view = 120

    nw = nt = actual_txt.strip()
    ow = ot = expected_txt.strip()
    if ot != nt:
        offset = 0
        while nt and ot and nt[:window] == ot[:window]:
            offset += window
            nt = nt[window:]
            ot = ot[window:]
        offset = max(offset - view, 0)
        print("   - - EXPECTED - -")
        print(ow[offset: offset + view + view])
        print("\n   - - ACTUAL - -")
        print(nw[offset: offset + view + view])
