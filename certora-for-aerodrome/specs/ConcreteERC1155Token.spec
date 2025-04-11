/**
 * # Simplified ERC1155 Spec (Clean)
 */

methods {
    function balanceOf(address, uint256) external returns (uint256) envfree;
    function isApprovedForAll(address, address) external returns (bool) envfree;
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

//// ## Edge Cases //////////////////////////////////////////////////////////

/// Self-transfer should not change balance
rule safeTransferToSelfKeepsBalanceUnchanged {
    env e;
    address from; uint256 id; uint256 amount;
    bytes data;

    require e.msg.sender == from;
    require balanceOf(from, id) >= amount;

    uint256 before = balanceOf(from, id);

    safeTransferFrom(e, from, from, id, amount, data);

    uint256 after = balanceOf(from, id);

    assert after == before,
        "Self-transfer should not change balance";
}

/// Transfer of zero tokens should not affect balances
rule safeTransferZeroAmountNoEffect {
    env e;
    address from; address to; uint256 id;
    bytes data;

    require e.msg.sender == from;
    require from != to;

    uint256 beforeFrom = balanceOf(from, id);
    uint256 beforeTo = balanceOf(to, id);

    safeTransferFrom(e, from, to, id, 0, data);

    uint256 afterFrom = balanceOf(from, id);
    uint256 afterTo = balanceOf(to, id);

    assert afterFrom == beforeFrom,
        "Sender's balance should remain the same on zero transfer";
    assert afterTo == beforeTo,
        "Recipient's balance should remain the same on zero transfer";
}

/// Transfer of full balance should zero out sender
rule safeTransferExactBalanceShouldZeroSender {
    env e;
    address from; address to; uint256 id;
    bytes data;

    require e.msg.sender == from;
    require from != to;

    uint256 amount = balanceOf(from, id);
    require amount > 0;

    safeTransferFrom(e, from, to, id, amount, data);

    assert balanceOf(from, id) == 0,
        "Sender's balance should be zero after full transfer";
}

//// ## Permissions //////////////////////////////////////////////////////////

/// Transfer should revert if sender is not owner nor approved
rule safeTransferRevertsIfNotApproved {
    env e;
    address from; address to; uint256 id; uint256 amount;
    bytes data;

    require e.msg.sender != from;
    require !isApprovedForAll(from, e.msg.sender);
    require balanceOf(from, id) >= amount;

    safeTransferFrom@withrevert(e, from, to, id, amount, data);

    assert lastReverted,
        "Should revert if sender is not owner nor approved operator";
}
