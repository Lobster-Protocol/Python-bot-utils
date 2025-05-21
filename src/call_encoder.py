"""EVM call data encoder module for python-bot-utils."""

from typing import Any, List, Sequence, TypedDict, Union, cast

import eth_abi
from web3 import Web3


class ABIInput(TypedDict):
    type: str
    name: str


class ABIFunction(TypedDict, total=False):
    type: str
    name: str
    inputs: List[ABIInput]


def encode_call(
    abi_or_signature: Union[List[ABIFunction], Sequence[ABIFunction], str],
    function_name: str,
    args: List[Any],
) -> str:
    """
    Encode an Ethereum contract function call.

    Args:
        abi_or_signature: Either a contract ABI (list/dict) or a
                         function signature string
                         (e.g., "transfer(address,uint256)")
        function_name: Name of the function to call
        args: List of arguments to pass to the function

    Returns:
        str: Encoded transaction data with 0x prefix

    Examples:
        >>> # Using function signature
        >>> encode_call(
        ...     "transfer(address,uint256)",
        ...     "transfer",
        ...     ["0x7B253B4f7d9D36d4eDBE558e0Fc24c1Dc071c036", 1000000]
        ... )
        '0xa9059cbb0000...'

        >>> # Using ABI
        >>> abi = [
        ...     {
        ...         "type": "function",
        ...         "name": "transfer",
        ...         "inputs": [
        ...             {"type": "address", "name": "to"},
        ...             {"type": "uint256", "name": "amount"}
        ...         ]
        ...     }
        ... ]
        >>> encode_call(
        ...     abi,
        ...     "transfer",
        ...     ["0x7B253B4f7d9D36d4eDBE558e0Fc24c1Dc071c036", 1000000]
        ... )
        '0xa9059cbb0000...'
    """
    # Case 1: ABI was provided
    param_types: List[str] = []
    function_signature: str = ""

    if isinstance(abi_or_signature, (list, dict)):
        abi = abi_or_signature

        # Find the function in the ABI
        function_def = None
        for item in abi:
            # Check each condition separately to avoid W503
            is_dict = isinstance(item, dict)
            has_function_type = is_dict and item.get("type") == "function"
            has_matching_name = (
                has_function_type and item.get("name") == function_name
            )  # noqa: E501

            if has_matching_name:
                function_def = cast(ABIFunction, item)
                break

        if not function_def:
            raise ValueError(f"Function '{function_name}' not found in ABI")

        # Extract parameter types
        param_types = [
            input_["type"] for input_ in function_def.get("inputs", [])
        ]  # noqa: E501

        # Construct function signature
        param_types_str = ",".join(param_types)
        function_signature = f"{function_name}({param_types_str})"

    # Case 2: Function signature was provided
    else:
        function_signature = str(abi_or_signature)
        # Extract parameter types from the signature
        signature_parts = function_signature.split("(")
        if len(signature_parts) > 1:
            param_section = signature_parts[1].rstrip(")")
            # Split long line to avoid E501
            if param_section:
                param_types = param_section.split(",")
            else:
                param_types = []

    # Get function selector (first 4 bytes of keccak hash)
    function_selector = Web3.keccak(text=function_signature)[:4].hex()

    # Process arguments
    processed_args: List[Any] = []
    for i, (type_, value) in enumerate(zip(param_types, args)):
        if type_ == "address":
            processed_args.append(Web3.to_checksum_address(value))
        # Handle uint/int types
        elif type_.startswith("uint"):
            # Ensure numeric values are integers
            if isinstance(value, str):
                processed_args.append(int(value))
            else:
                processed_args.append(value)
        elif type_.startswith("int"):
            # Ensure numeric values are integers
            if isinstance(value, str):
                processed_args.append(int(value))
            else:
                processed_args.append(value)
        else:
            processed_args.append(value)

    # Encode parameters
    encoded_params = eth_abi.encode(param_types, processed_args).hex()

    # Combine selector with encoded parameters
    encoded_data = f"0x{function_selector}{encoded_params}"

    return encoded_data
