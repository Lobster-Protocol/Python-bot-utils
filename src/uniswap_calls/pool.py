"""Uniswap V3 function encoder."""

# todo: test
from typing import cast

from .call_encoder import encode_call


def encode_mint(
    owner: str,
    tick_lower: int,
    tick_upper: int,
    liquidity: int,
) -> str:
    """Encode a call to the Uniswap V3 pool mint function, avoiding the position manager.

    (position owner won't receive a position nft)

    Args:
        owner: The address that will own the position
        tick_lower: The lower tick of the position
        tick_upper: The upper tick of the position
        amount: The desired amount of liquidity to mint
        data: Callback data to be passed to the callback function

    Returns:
        str: Encoded call data with 0x prefix

    Example:
        >>> encode_mint(
        ...     owner="0x742d35Cc6634C0532925a3b8D03c8C0B6B1A2b68",
        ...     tick_lower=-887272,  # Example lower tick
        ...     tick_upper=887272,   # Example upper tick
        ...     amount=1000000000000000000,  # liquidity amount
        ...     data="0x...." # Example callback data
    """
    print(owner, tick_lower, tick_upper, liquidity)
    raise NotImplementedError("The mint function encoder is not implemented yet. ")


def encode_burn(tick_lower: int, tick_upper: int, liquidity: int) -> str:
    """Encode a call to the Uniswap V3 pool burn function.

    Burns liquidity for a specific position

    Args:
        tick_lower: The lower tick of the position
        tick_upper: The upper tick of the position
        amount: The amount of liquidity to burn

    Returns:
        str: Encoded call data with 0x prefix

    Example:
        >>> encode_burn(-87272, 87272, 10000000000000000)
        '0x42966c68...'
    """
    # Uniswap V3 burn function signature
    burn_signature = "burn(int24,int24,uint128)"

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=burn_signature,
            function_name="burn",
            args=[tick_lower, tick_upper, liquidity],
        ),
    )


def encode_collect(
    recipient: str,
    tickLower: int,
    tickUpper: int,
    amount0Requested: int,
    amount1Requested: int,
) -> str:
    """Encode a call to the Uniswap V3 pool collect function.

    Collects up to a maximum amount of fees owed to a specific position to the recipient.
    This function collects accumulated fees from a liquidity position.

    Args:
        recipient: The account that should receive the tokens
        tickLower: The lower tick of the position
        tickUpper: The upper tick of the position
        amount0Requested: The maximum amount of token0 to collect
        amount1Requested: The maximum amount of token1 to collect

    Returns:
        str: Encoded call data with 0x prefix

    Example:
        >>> encode_collect(
        ...     recipient="0x742d35Cc6634C0532925a3b8D03c8C0B6B1A2b68",
        ...     tickLower=-887272,  # Example lower tick
        ...     tickUpper=887272,   # Example upper tick
        ...     amount0Requested=340282366920938463463374607431768211455,  # Max uint128
        ... )
        '0xfc6f7865...'
    """
    # Uniswap V3 collect function signature
    collect_signature = "collect(" "(address,int24,int24,uint128,uint128)" ")"

    # Pack all parameters into a tuple (struct)
    collect_params = (
        recipient,
        tickLower,
        tickUpper,
        amount0Requested,
        amount1Requested,
    )

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=collect_signature,
            function_name="collect",
            args=[collect_params],
        ),
    )
