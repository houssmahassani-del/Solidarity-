// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SpectralHashVerifier
/// @notice Verify sha256(header || nonce) meets a toy difficulty (leading zero bytes).
contract SpectralHashVerifier {
    event CandidateTested(address indexed sender, bytes32 hashValue, bool success, uint8 leadingZeroBytes);

    /// @notice Test a candidate integer nonce concatenated with a header string.
    /// @param header The header string (off-chain you used this same header).
    /// @param nonce  The integer candidate (converted to string in abi.encodePacked).
    /// @param requireZeroBytes number of leading zero *bytes* required (toy difficulty).
    function testCandidate(string calldata header, uint256 nonce, uint8 requireZeroBytes) external {
        bytes memory payload = abi.encodePacked(header, uintToString(nonce));
        bytes32 h = sha256(payload);

        // Count leading zero bytes
        uint8 zeros = leadingZeroBytes(h);
        bool success = zeros >= requireZeroBytes;

        emit CandidateTested(msg.sender, h, success, zeros);
    }

    /// @dev Helper: count leading zero bytes in bytes32
    function leadingZeroBytes(bytes32 data) internal pure returns (uint8) {
        uint8 count = 0;
        // iterate over bytes from most-significant (index 0) to least
        for (uint i = 0; i < 32; i++) {
            bytes1 b = data[i]; // use bytes1 (not 'byte')
            if (b == 0x00) {
                unchecked { count++; } // safe, max 32
            } else {
                break;
            }
        }
        return count;
    }

    /// @dev Convert uint to decimal string
    function uintToString(uint v) internal pure returns (string memory str) {
        if (v == 0) return "0";
        uint maxlength = 100;
        bytes memory reversed = new bytes(maxlength);
        uint i = 0;
        while (v != 0) {
            uint remainder = v % 10;
            v = v / 10;
            reversed[i++] = bytes1(uint8(48 + remainder));
        }
        bytes memory s = new bytes(i);
        for (uint j = 0; j < i; j++) {
            s[j] = reversed[i - 1 - j];
        }
        str = string(s);
    }
}