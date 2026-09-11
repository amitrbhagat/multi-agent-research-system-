from unittest.mock import AsyncMock

import pytest

from app.tools.retry_utils import with_retry


@pytest.mark.asyncio
async def test_retry_succeeds_after_transient_failures():
    call_count = {"n": 0}

    @with_retry(max_attempts=3)
    async def flaky_call():
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise ConnectionError("simulated failure")
        return "success"

    result = await flaky_call()
    assert result == "success"
    assert call_count["n"] == 3


@pytest.mark.asyncio
async def test_retry_gives_up_after_max_attempts():
    @with_retry(max_attempts=3)
    async def always_fails():
        raise ConnectionError("simulated permanent failure")

    with pytest.raises(ConnectionError):
        await always_fails()



if __name__ == "__main__":
    test_retry_succeeds_after_transient_failures()
    test_retry_gives_up_after_max_attempts()
