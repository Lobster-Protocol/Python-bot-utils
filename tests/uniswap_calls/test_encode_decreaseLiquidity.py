"""Tests for Uniswap V3 decreaseLiquidity function encoder."""

from uniswap_calls.position_manager import encode_decreaseLiquidity


def test_encode_decreaseLiquidity() -> None:
    """Function: decreaseLiquidity(tuple params).

    MethodID: 0x0c49ccbe
    [0]:  00000000000000000000000000000000000000000000000000000000000306fc
    [1]:  00000000000000000000000000000000000000000000000000000168372abefa
    [2]:  0000000000000000000000000000000000000000000000000000000000000000
    [3]:  0000000000000000000000000000000000000000000000000000000000000000
    [4]:  0000000000000000000000000000000000000000000000000000000068396ac4
    """
    token_id: int = 198396
    liquidity: int = 1547113774842
    amount0_min: int = 0
    amount1_min: int = 0
    deadline: int = 1748593348

    encoded_call: str = encode_decreaseLiquidity(
        token_id=token_id,
        liquidity=liquidity,
        amount0_min=amount0_min,
        amount1_min=amount1_min,
        deadline=deadline,
    )
    assert isinstance(encoded_call, str)
    # Ensure the encoded call is the same as the expected value
    expected_call: str = (
        "0x0c49ccbe00000000000000000000000000000000000000000000000000000000000306fc00000000000000000000000000000000000000000000000000000168372abefa000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000068396ac4"  # noqa
    )
    assert (
        encoded_call == expected_call
    ), f"Expected {expected_call}, got {encoded_call}"
