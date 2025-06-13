pragma solidity >=0.4.22 <0.9.0;
    contract DispatchContract {
    string public uniqueID;
	int public lotNumber;
	
    
    function perform_transactions(string memory _uniqueID, int _lotNumber) public{
       uniqueID = _uniqueID;
		lotNumber = _lotNumber;
		
    }
        
}
