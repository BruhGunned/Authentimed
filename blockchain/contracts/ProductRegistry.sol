// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract ProductRegistry {

    enum State { NONE, VALID, REPLAYED }

    struct Product {
        address manufacturer;
        State state;
    }

    mapping(string => Product) private products;

    // Manufacturer approval
    mapping(address => bool) public approvedManufacturers;
    mapping(address => uint256) public votes;

    // Canonical template hash
    mapping(address => bytes32) public packagingHash;

    // Validators (PBFT-style)
    mapping(address => bool) public validators;
    uint256 public validatorCount;

    constructor(address[] memory _validators) {
        for (uint i = 0; i < _validators.length; i++) {
            validators[_validators[i]] = true;
        }
        validatorCount = _validators.length;
    }

    modifier onlyValidator() {
        require(validators[msg.sender], "Not validator");
        _;
    }

    modifier onlyApprovedManufacturer() {
        require(approvedManufacturers[msg.sender], "Manufacturer not approved");
        _;
    }

    // -------------------------
    // PBFT-style manufacturer approval
    // -------------------------

    function voteManufacturer(address candidate) public onlyValidator {
        votes[candidate]++;

        if (votes[candidate] >= (validatorCount * 2 / 3) + 1) {
            approvedManufacturers[candidate] = true;
        }
    }

    // -------------------------
    // Register canonical template
    // -------------------------

    function registerTemplateHash(bytes32 hash)
        public
        onlyApprovedManufacturer
    {
        packagingHash[msg.sender] = hash;
    }

    // -------------------------
    // Register product
    // -------------------------

    function registerProduct(string memory id)
        public
        onlyApprovedManufacturer
    {
        require(products[id].state == State.NONE, "Already registered");

        products[id] = Product({
            manufacturer: msg.sender,
            state: State.VALID
        });
    }

    // -------------------------
    // 🔥 Replay Detection Here
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
