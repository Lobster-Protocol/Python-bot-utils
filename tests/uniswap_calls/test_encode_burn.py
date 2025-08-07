"""Tests for Uniswap V3 mint function encoder."""

from uniswap_calls.position_manager import encode_burn


def test_encode_burn() -> None:
    """Function: burn(uint256 _tokenId).

    MethodID: 0x42966c68
    [0]: 00000000000000000000000000000000000000000000000000000000000306fb

    Raw: 0x42966c6800000000000000000000000000000000000000000000000000000000000306fb
    Token ID to burn: 198395
    """
    token_id: int = 198395

    encoded_call: str = encode_burn(token_id=token_id)

    assert isinstance(encoded_call, str)

    # Ensure the encoded call is the same as the expected value
    expected_call: str = (
        "0x42966c6800000000000000000000000000000000000000000000000000000000000306fb"
    )

    assert (
        encoded_call == expected_call
    ), f"Expected {expected_call}, got {encoded_call}"
