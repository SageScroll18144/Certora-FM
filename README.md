# ERC-1155 Transfer Specification — Certora Rules

This specification verifies the correct behavior of the `safeTransferFrom` function in an ERC-1155 token contract using Certora Prover. The rules are written in CVL (Certora Verification Language) and cover core functionality, edge cases, and permission enforcement.

---

## ✅ Rules Overview

### `safeTransferShouldUpdateBalances`

**Purpose:**  
Ensures that when a valid transfer is made, the sender’s balance decreases and the recipient’s balance increases by the correct amount.

**Conditions:**
- Sender must be the transaction initiator.
- Sender and recipient must be different.
- Sender must have a sufficient balance.

**Assertions:**
- Sender's balance is reduced by the transferred amount.
- Recipient's balance is increased by the transferred amount.

---

### `safeTransferRevertsIfInsufficientBalance`

**Purpose:**  
Verifies that a transfer is correctly reverted if the sender attempts to send more tokens than they own.

**Conditions:**
- Sender is the transaction initiator.
- Sender’s balance is less than the transfer amount.

**Assertions:**
- The transfer must revert.

---

## 🧪 Edge Case Rules

### `safeTransferToSelfKeepsBalanceUnchanged`

**Purpose:**  
Ensures that transferring tokens to oneself does not affect the token balance.

**Conditions:**
- Sender is the transaction initiator.
- Sender has enough tokens to transfer.

**Assertions:**
- Balance remains unchanged after the transfer.

---

### `safeTransferZeroAmountNoEffect`

**Purpose:**  
Ensures that transferring zero tokens does not alter the balances of either the sender or recipient.

**Conditions:**
- Sender is the transaction initiator.
- Sender and recipient are different.

**Assertions:**
- Both sender and recipient balances remain unchanged.

---

### `safeTransferExactBalanceShouldZeroSender`

**Purpose:**  
Ensures that transferring exactly the full balance of a token results in the sender's balance becoming zero.

**Conditions:**
- Sender is the transaction initiator.
- Sender and recipient are different.
- Sender has a non-zero balance.

**Assertions:**
- Sender's balance becomes zero after the transfer.

---

## 🔐 Permission Rules

### `safeTransferRevertsIfNotApproved`

**Purpose:**  
Ensures that transfers initiated by non-owners who are not approved as operators are correctly reverted.

**Conditions:**
- Sender is **not** the token owner.
- Sender is **not** approved as an operator.
- Token owner has sufficient balance.

**Assertions:**
- The transfer must revert.

---

