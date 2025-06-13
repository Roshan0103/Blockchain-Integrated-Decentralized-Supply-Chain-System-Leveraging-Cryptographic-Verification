pragma solidity >=0.4.22 <0.9.0;
    contract ProductionReceiptsContract {
    string public uniqueID;
	string public productID;
	int public lotNumber;
	
    
    function perform_transactions(string memory _uniqueID, string memory _productID, int _lotNumber) public{
       uniqueID = _uniqueID;
		productID = _productID;
		lotNumber = _lotNumber;
		
    }
        
}
