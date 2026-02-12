// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;


contract ProductRegistry {

    enum State { NONE, VALID, DUPLICATE, REPLAYED }

    mapping(string => State) private products;

    address public manufacturer;

    constructor() {
        manufacturer = msg.sender;
    }

    modifier onlyManufacturer() {
        require(msg.sender == manufacturer, "Not authorized");
        _;
    }

    function registerProduct(string memory id) public onlyManufacturer {
        require(products[id] == State.NONE, "Already registered");
        products[id] = State.VALID;
    }

    function markDuplicate(string memory id) public onlyManufacturer {
        require(products[id] == State.VALID, "Not valid product");
        products[id] = State.DUPLICATE;
    }

    function verifyProduct(string memory id) public returns (bool) {
    if (products[id] == State.VALID) {
        products[id] = State.REPLAYED;
        return true;
    }
    return false;
}

    function getProductState(string memory id) public view returns (State) {
        return products[id];
    }

}
