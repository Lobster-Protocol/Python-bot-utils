"""EVM call data encoder module for python-bot-utils - Fixed version."""

import re
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


def parse_function_signature(signature: str) -> tuple[str, List[str]]:
    """
    Parse a function signature to extract function name and parameter types.

    Handles nested parentheses for tuple/struct types.

    Args:
        signature: Function signature like "mint((address,uint256),uint256)"

    Returns:
        tuple: (function_name, parameter_types_list)
    """
    # Extract function name
    match = re.match(r"^(\w+)\((.*)\)$", signature)
    if not match:
        raise ValueError(f"Invalid function signature: {signature}")

    function_name = match.group(1)
    params_str = match.group(2)

    if not params_str:
        return function_name, []

    # Parse parameter types, handling nested parentheses
    param_types = []
    current_param = ""
    paren_depth = 0

    for char in params_str:
        if char == "(":
            paren_depth += 1
            current_param += char
        elif char == ")":
            paren_depth -= 1
            current_param += char
        elif char == "," and paren_depth == 0:
            # We're at the top level and found a comma
            # - end of current parameter
            param_types.append(current_param.strip())
            current_param = ""
        else:
            current_param += char

    # Add the last parameter
    if current_param.strip():
        param_types.append(current_param.strip())

    return function_name, param_types


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
        (e.g., "transfer(address,uint256)" or "mint((address,uint256),uint256)")
        function_name: Name of the function to call
        args: List of arguments to pass to the function

    Returns:
        str: Encoded call data with 0x prefix

    Examples:
        >>> # Using function signature
        >>> encode_call(
        ...     "transfer(address,uint256)",
        ...     "transfer",
        ...     ["0x7B253B4f7d9D36d4eDBE558e0Fc24c1Dc071c036", 1000000]
        ... )
        '0xa9059cbb0000...'

        >>> # Using function signature with tuple/struct
        >>> encode_call(
        ...     "mint((address,address,uint24,int24,int24,uint256,uint256,uint256,uint256,address,uint256))",
        ...     "mint",
        ...     [("0x1234...", "0x5678...", 3000, -887220, 887220, 1000, 1000, 950, 950, "0xabcd...", 1640995200)]
        ... )
        '0x88316456...'

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
        # FIXED: Use the new parser that handles nested parentheses
        parsed_name, param_types = parse_function_signature(function_signature)

        # Verify the function name matches
        if parsed_name != function_name:
            raise ValueError(
                f"Function name mismatch: signature has '{parsed_name}' but expected '{function_name}'"
            )

    # Get function selector (first 4 bytes of keccak hash)
    function_selector = Web3.keccak(text=function_signature)[:4].hex()

    # Process arguments - Enhanced to handle tuple types
    processed_args: List[Any] = []
    for i, (type_, value) in enumerate(zip(param_types, args)):
        processed_arg = process_argument(type_, value)
        processed_args.append(processed_arg)

    # Encode parameters
    try:
        encoded_params = eth_abi.encode(param_types, processed_args).hex()
    except Exception as e:
        print(f"Error encoding parameters: {e}")
        print(f"Parameter types: {param_types}")
        print(f"Processed arguments: {processed_args}")
        raise

    # Combine selector with encoded parameters
    encoded_data = f"0x{function_selector}{encoded_params}"
    return encoded_data


def process_argument(type_: str, value: Any) -> Any:
    """
    Process a single argument based on its type.

    Args:
        type_: The Solidity type (e.g., "address", "uint256", "(address,uint256)")
        value: The value to process

    Returns:
        Processed value suitable for eth_abi.encode
    """
    if type_ == "address":
        return Web3.to_checksum_address(value)

    # Handle uint/int types
    elif type_.startswith("uint") or type_.startswith("int"):
        # Ensure numeric values are integers
        if isinstance(value, str):
            return int(value)
        else:
            return value

    # Handle tuple types (structs)
    elif type_.startswith("(") and type_.endswith(")"):
        if not isinstance(value, (tuple, list)):
            raise ValueError(f"Expected tuple/list for type {type_}, got {type(value)}")

        # Parse the tuple type to get individual field types
        inner_types_str = type_[1:-1]  # Remove outer parentheses
        inner_types = []
        current_type = ""
        paren_depth = 0

        for char in inner_types_str:
            if char == "(":
                paren_depth += 1
                current_type += char
            elif char == ")":
                paren_depth -= 1
                current_type += char
            elif char == "," and paren_depth == 0:
                inner_types.append(current_type.strip())
                current_type = ""
            else:
                current_type += char

        if current_type.strip():
            inner_types.append(current_type.strip())

        # Process each field in the tuple
        processed_tuple = []
        for field_type, field_value in zip(inner_types, value):
            processed_field = process_argument(field_type, field_value)
            processed_tuple.append(processed_field)

        return tuple(processed_tuple)

    # Handle array types
    elif type_.endswith("[]"):
        if not isinstance(value, (list, tuple)):
            raise ValueError(
                f"Expected list/tuple for array type {type_}, got {type(value)}"
            )

        element_type = type_[:-2]  # Remove "[]"
        return [process_argument(element_type, item) for item in value]

    # Default: return as-is
    else:
        return value
