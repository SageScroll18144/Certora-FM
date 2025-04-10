/**
 * # Simplified ERC1155 Spec (Clean)
 */

methods {
    function balanceOf(address, uint256) external returns (uint256) envfree;
    function safeTransferFrom(address, address, uint256, uint256, bytes) external;
}

//// ## Basic Rules //////////////////////////////////////////////////////////

/// Transfer should move the amount from sender to recipient
rule safeTransferShouldUpdateBalances {
    env e;
    address from; address to; uint256 id; uint256 amount;
    bytes data;

    require e.msg.sender == from;
    require from != to;

    uint256 beforeFrom = balanceOf(from, id);
    uint256 beforeTo = balanceOf(to, id);

    require beforeFrom >= amount;

    safeTransferFrom(e, from, to, id, amount, data);

    uint256 afterFrom = balanceOf(from, id);
    uint256 afterTo = balanceOf(to, id);

    assert afterFrom == beforeFrom - amount,
        "Sender balance should decrease by amount";
    assert afterTo == beforeTo + amount,
        "Recipient balance should increase by amount";
}

/// Transfer should revert if sender lacks balance
rule safeTransferRevertsIfInsufficientBalance {
    env e;
    address from; address to; uint256 id; uint256 amount;
    bytes data;

    require e.msg.sender == from;
    require balanceOf(from, id) < amount;

    safeTransferFrom@withrevert(e, from, to, id, amount, data);

    assert lastReverted,
        "Should revert if from doesn't have enough tokens";
}
