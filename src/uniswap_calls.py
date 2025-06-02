"""Uniswap V3 function encoder."""

# todo: add: "exactOutputSingle","exactInput" and "exactOutput" function encoders

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


def encode_burn(token_id: int) -> str:
    """Encode a call to the Uniswap V3 NonfungiblePositionManager burn function.

    Burns a token ID, which deletes it from the NFT contract. The token must
    have 0 liquidity and all tokens must be collected first.

    Args:
        token_id: The ID of the token that is being burned

    Returns:
        str: Encoded transaction data with 0x prefix

    Example:
        >>> encode_burn(token_id=12345)
        '0x42966c68...'
    """
    # Uniswap V3 burn function signature
    burn_signature = "burn(uint256)"

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=burn_signature, function_name="burn", args=[token_id]
        ),
    )


def encode_increaseLiquidity(
    token_id: int,
    amount0_desired: int,
    amount1_desired: int,
    amount0_min: int,
    amount1_min: int,
    deadline: int,
) -> str:
    """Encode a call to the Uniswap V3 NonfungiblePositionManager increaseLiquidity function.

    Increases the amount of liquidity in a position, with tokens paid by the msg.sender.
    The position must already exist and have some liquidity.

    Args:
        token_id: The ID of the token for which liquidity is being increased
        amount0_desired: The desired amount of token0 to be spent
        amount1_desired: The desired amount of token1 to be spent
        amount0_min: The minimum amount of token0 to spend (slippage protection)
        amount1_min: The minimum amount of token1 to spend (slippage protection)
        deadline: The time by which the transaction must be included

    Returns:
        str: Encoded transaction data with 0x prefix

    Example:
        >>> encode_increaseLiquidity(
        ...     token_id=12345,
        ...     amount0_desired=1000000000000000000,    # 1 token with 18 decimals
        ...     amount1_desired=1000000000000000000,    # 1 token with 18 decimals
        ...     amount0_min=950000000000000000,         # Min token0 (5% slippage protection)
        ...     amount1_min=950000000000000000,         # Min token1 (5% slippage protection)
        ...     deadline=1640995200                     # Unix timestamp
        ... )
        '0x219f5d17...'
    """
    # Uniswap V3 increaseLiquidity function signature
    increase_liquidity_signature = (
        "increaseLiquidity(" "(uint256,uint256,uint256,uint256,uint256,uint256)" ")"
    )

    # Pack all parameters into a tuple (struct)
    increase_liquidity_params = (
        token_id,
        amount0_desired,
        amount1_desired,
        amount0_min,
        amount1_min,
        deadline,
    )

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=increase_liquidity_signature,
            function_name="increaseLiquidity",
            args=[increase_liquidity_params],
        ),
    )


def encode_decreaseLiquidity(
    token_id: int,
    liquidity: int,
    amount0_min: int,
    amount1_min: int,
    deadline: int,
) -> str:
    """Encode a call to the Uniswap V3 NonfungiblePositionManager decreaseLiquidity function.

    Decreases the amount of liquidity in a position and accounts it to the position.
    The liquidity is burned and the underlying tokens are accounted to the position's tokens owed.

    Args:
        token_id: The ID of the token for which liquidity is being decreased
        liquidity: The amount by which liquidity will be decreased
        amount0_min: The minimum amount of token0 that should be accounted for the burned liquidity
        amount1_min: The minimum amount of token1 that should be accounted for the burned liquidity
        deadline: The time by which the transaction must be included

    Returns:
        str: Encoded transaction data with 0x prefix

    Example:
        >>> encode_decreaseLiquidity(
        ...     token_id=12345,
        ...     liquidity=1000000000000000000,        # Amount of liquidity to decrease
        ...     amount0_min=950000000000000000,       # Min token0 (5% slippage protection)
        ...     amount1_min=950000000000000000,       # Min token1 (5% slippage protection)
        ...     deadline=1640995200                   # Unix timestamp
        ... )
        '0x0c49ccbe...'
    """
    # Uniswap V3 decreaseLiquidity function signature
    decrease_liquidity_signature = (
        "decreaseLiquidity(" "(uint256,uint128,uint256,uint256,uint256)" ")"
    )

    # Pack all parameters into a tuple (struct)
    decrease_liquidity_params = (
        token_id,
        liquidity,
        amount0_min,
        amount1_min,
        deadline,
    )

    # Use the encode_call function to encode the transaction
    return cast(
        str,
        encode_call(
            abi_or_signature=decrease_liquidity_signature,
            function_name="decreaseLiquidity",
            args=[decrease_liquidity_params],
        ),
    )


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
        str: Encoded transaction data with 0x prefix

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
