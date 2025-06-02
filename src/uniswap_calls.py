"""Uniswap V3 function encoder."""

from typing import cast

from call_encoder import encode_call


def encode_mint(
    token0: str,
    token1: str,
    fee: int,
    tick_lower: int,
    tick_upper: int,
    amount0_desired: int,
    amount1_desired: int,
    amount0_min: int,
    amount1_min: int,
    recipient: str,
    deadline: int,
) -> str:
    """Encode a call to the Uniswap V3 NonfungiblePositionManager mint function.

    Args:
        token0: Address of the first token in the pool
        token1: Address of the second token in the pool
        fee: The fee tier of the pool (e.g., 3000 for 0.3%, 10000 for 1%)
        tick_lower: The lower tick of the position
        tick_upper: The upper tick of the position
        amount0_desired: The desired amount of token0 to be spent
        amount1_desired: The desired amount of token1 to be spent
        amount0_min: The minimum amount of token0 to spend
        amount1_min: The minimum amount of token1 to spend
        recipient: The address that will receive the NFT
        deadline: The time by which the transaction must be included

    Returns:
        str: Encoded transaction data with 0x prefix

    Example:
        >>> encode_mint(
        ...     token0="0xA0b86a33E6441cC0c34d090e6C36AE30F2A5EF37",
        ...     token1="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        ...     fee=3000,
        ...     tick_lower=-887220,
        ...     tick_upper=887220,
        ...     amount0_desired=1000000000000000000,  # 1 token with 18 decimals
        ...     amount1_desired=1000000000000000000,  # 1 token with 18 decimals
        ...     amount0_min=950000000000000000,       # 0.95 token (5% slippage)
        ...     amount1_min=950000000000000000,       # 0.95 token (5% slippage)
        ...     recipient="0x742d35Cc6634C0532925a3b8D03c8C0B6B1A2b68",
        ...     deadline=1640995200  # Unix timestamp
        ... )
        '0x88316456...'
    """
    # Uniswap V3 mint function signature
    mint_signature = (
        "mint("
        "(address,address,uint24,int24,int24,uint256,uint256,uint256,uint256,address,uint256)"
        ")"
    )

    # Pack all parameters into a tuple (struct)
    mint_params = (
        token0,
        token1,
        fee,
        tick_lower,
        tick_upper,
        amount0_desired,
        amount1_desired,
        amount0_min,
        amount1_min,
        recipient,
        deadline,
    )

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=mint_signature, function_name="mint", args=[mint_params]
        ),
    )
