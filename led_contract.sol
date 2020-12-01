// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.8.0;

contract LedContract {
    
    int8 public on;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function setLed(int8 newOn) public payable {
        on = newOn;
    }
    
    function readLed() public view returns (int8) {
        return on;
    }
    
    function retrieveEther() public returns (bool) {
        require(msg.sender == owner, "Only the owner of the contract can retrieve ether.");
        uint amount = address(this).balance;
        if (amount > 0) {
            if (!msg.sender.send(amount)) {
                return false;
            }
        }
        return true;
    }
    
    function kill() public {
        require(msg.sender == owner, "Only the owner of the contract is able to kill.");
        selfdestruct(msg.sender);
    }
}
