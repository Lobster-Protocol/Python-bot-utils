from typing import cast

from ..call_encoder import encode_call

# todo: add: "exactOutputSingle","exactInput" and "exactOutput" function encoders


def encode_exactInputSingle(
    token_in: str,
    token_out: str,
    fee: int,
    recipient: str,
    deadline: int,
    amount_in: int,
    amount_out_minimum: int,
    sqrt_price_limit_x96: int,
) -> str:
    """Encode a call to the Uniswap V3 SwapRouter exactInputSingle function.

    Swaps a fixed amount of one token for a maximum possible amount of another token.
    This is a single-hop swap (direct swap between two tokens in one pool).

    Args:
        token_in: The contract address of the input token
        token_out: The contract address of the output token
        fee: The fee tier of the pool (e.g., 3000 for 0.3%, 10000 for 1%)
        recipient: The address that will receive the output tokens
        deadline: The time by which the transaction must be included
        amount_in: The exact amount of input tokens to be swapped
        amount_out_minimum: The minimum amount of output tokens (slippage protection)
        sqrt_price_limit_x96: The price limit in sqrt(price) * 2^96 format (0 for no limit)

    Returns:
        str: Encoded call data with 0x prefix

    Example:
        >>> encode_exactInputSingle(
        ...     token_in="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",      # WETH
        ...     token_out="0xA0b86a33E6441cC0c34d090e6C36AE30F2A5EF37",     # Token
        ...     fee=3000,                                                   # 0.3%
        ...     recipient="0x742d35Cc6634C0532925a3b8D03c8C0B6B1A2b68",
        ...     deadline=1640995200,                                        # Unix timestamp
        ...     amount_in=1000000000000000000,                              # 1 WETH
        ...     amount_out_minimum=950000000000000000,                      # Min output (5% slippage)
        ...     sqrt_price_limit_x96=0                                      # No price limit
        ... )
        '0x414bf389...'
    """
    # Uniswap V3 exactInputSingle function signature
    exact_input_single_signature = (
        "exactInputSingle("
        "(address,address,uint24,address,uint256,uint256,uint256,uint160)"
        ")"
    )

    # Pack all parameters into a tuple (struct)
    exact_input_single_params = (
        token_in,
        token_out,
        fee,
        recipient,
        deadline,
        amount_in,
        amount_out_minimum,
        sqrt_price_limit_x96,
    )

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=exact_input_single_signature,
            function_name="exactInputSingle",
            args=[exact_input_single_params],
        ),
    )
