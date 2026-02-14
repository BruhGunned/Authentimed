// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract ProductRegistry {

    enum State { NONE, VALID, REPLAYED }

    struct Product {
        address manufacturer;
        State state;
    }

    mapping(string => Product) private products;
    mapping(address => bytes32) public packagingHash;

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    // -------------------------
    // Register canonical template
    // -------------------------

    function registerTemplateHash(bytes32 hash)
        public
        onlyOwner
    {
        packagingHash[msg.sender] = hash;
    }

    // -------------------------
    // Register product
    // -------------------------

    function registerProduct(string memory id)
        public
        onlyOwner
    {
        require(products[id].state == State.NONE, "Already registered");

        products[id] = Product({
            manufacturer: msg.sender,
            state: State.VALID
        });
    }

    // -------------------------
    // Replay detection
    // -------------------------

    function verifyProduct(string memory id)
        public
        returns (bool)
    {
        if (products[id].state == State.VALID) {
            products[id].state = State.REPLAYED;
            return true;
        }

        return false;
    }

    function getProductState(string memory id)
        public
        view
        returns (State)
    {
        return products[id].state;
    }

    function getManufacturer(string memory id)
        public
        view
        returns (address)
    {
        return products[id].manufacturer;
    }

    function getTemplateHash(address manuf)
        public
        view
        returns (bytes32)
    {
        return packagingHash[manuf];
    }
}
