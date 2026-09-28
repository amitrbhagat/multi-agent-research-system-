# eval/evaluators.py

def check_route(final_state: dict, expected_route: str) -> bool:
    """Did the query hit the expected branch of the graph?"""
    if expected_route == "data_analyst":
        return bool(final_state.get("analyst_result", {}).get("value") is not None
                    or final_state.get("analyst_result", {}).get("answer"))
    if expected_route == "research":
        return bool(final_state.get("draft"))
    return False


def check_min_citations(final_state: dict, min_count: int) -> bool:
    """Does the draft cite at least min_count distinct, non-null sources?"""
    claims = final_state.get("claims", [])
    cited_sources = {c["source_id"] for c in claims if c.get("source_id")}
    return len(cited_sources) >= min_count


def check_allow_ungrounded_admission(final_state: dict) -> bool:
    """
    For sparse-data queries, success means the Writer/Critic honestly
    flagged the gap (via ungrounded_claims or an explicit 'insufficient
    information' style draft) rather than confidently fabricating.
    """
    ungrounded = final_state.get("critique", {}).get("ungrounded_claims", [])
    draft = final_state.get("draft", "").lower()
    admits_gap = any(
        phrase in draft
        for phrase in ("don't have", "couldn't find", "insufficient", "not available", "no information")
    )
    return bool(ungrounded) or admits_gap


def check_should_not_crash(final_state: dict) -> bool:
    """Minimal bar: the graph returned a final_state at all, no exception."""
    return final_state is not None


EVALUATOR_MAP = {
    "route": check_route,
    "min_citations": check_min_citations,
    "allow_ungrounded_admission": lambda state, _: check_allow_ungrounded_admission(state),
    "should_not_crash": lambda state, _: check_should_not_crash(state),
}