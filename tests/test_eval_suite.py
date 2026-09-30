from eval.run_eval import run_eval_suite


def test_eval_suite_runs_without_crashing():
    """
    Not asserting a specific pass rate here (that varies as you tune
    the system) — just confirming the eval harness itself is functional
    and returns valid counts, since a broken eval script is worse than
    no eval script (false confidence).
    """
    passed, total = run_eval_suite()
    assert total == 12  # matches len(GOLDEN_QUERIES) — update if you add more
    assert 0 <= passed <= total