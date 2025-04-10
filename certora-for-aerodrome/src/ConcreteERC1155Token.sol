// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol"; // Caminho pode variar conforme seu projeto;

contract ConcreteERC1155Token is ERC1155 {
    address public owner;

    uint256 public constant GOLD = 1;

    constructor(string memory uri_) ERC1155(uri_) {
        owner = msg.sender;

        _mint(msg.sender, GOLD, 1000, ""); // Mint 1000 unidades do token GOLD para o deployer
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    function mint(address to, uint256 id, uint256 amount, bytes memory data) public onlyOwner {
        _mint(to, id, amount, data);
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) public onlyOwner {
        _mintBatch(to, ids, amounts, data);
    }

    function burn(address from, uint256 id, uint256 amount) public {
        require(
            from == msg.sender || isApprovedForAll(from, msg.sender),
            "Caller is not owner nor approved"
        );
        _burn(from, id, amount);
    }

    function burnBatch(address from, uint256[] memory ids, uint256[] memory amounts) public {
        require(
            from == msg.sender || isApprovedForAll(from, msg.sender),
            "Caller is not owner nor approved"
        );
        _burnBatch(from, ids, amounts);
    }
}
