"""Tests for Uniswap V3 collect function encoder."""

from uniswap_calls.position_manager import encode_collect


def test_encode_collect() -> None:
    """Function: collect(tuple params).

    MethodID: 0xfc6f7865
    [0]:  00000000000000000000000000000000000000000000000000000000000f4713
    [1]:  000000000000000000000000e317d37afb4ea9882e09e83fa3742723d789f0c3
    [2]:  00000000000000000000000000000000ffffffffffffffffffffffffffffffff
    [3]:  00000000000000000000000000000000ffffffffffffffffffffffffffffffff
    """
    token_id: int = 1001235
    recipient: str = "0xe317d37afb4ea9882e09e83fa3742723d789f0c3"
    amount0_max: int = 340282366920938463463374607431768211455
    amount1_max: int = 340282366920938463463374607431768211455

    encoded_call: str = encode_collect(
        token_id=token_id,
        recipient=recipient,
        amount0_max=amount0_max,
        amount1_max=amount1_max,
    )
    assert isinstance(encoded_call, str)
    # Ensure the encoded call is the same as the expected value
    expected_call: str = (
        "0xfc6f786500000000000000000000000000000000000000000000000000000000000f4713000000000000000000000000e317d37afb4ea9882e09e83fa3742723d789f0c300000000000000000000000000000000ffffffffffffffffffffffffffffffff00000000000000000000000000000000ffffffffffffffffffffffffffffffff"  # noqa
    )
    assert (
        encoded_call == expected_call
    ), f"Expected {expected_call}, got {encoded_call}"
