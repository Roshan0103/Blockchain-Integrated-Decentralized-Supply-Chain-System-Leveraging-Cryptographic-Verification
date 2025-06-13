pragma solidity >=0.4.22 <0.9.0;
    contract ProductTrackingContract {
    string public uniqueID;
	string public productID;
	int public productUniqueIdentifier;
	int public lotNumber;
	
    
    function perform_transactions(string memory _uniqueID, string memory _productID, int _productUniqueIdentifier, int _lotNumber) public{
       uniqueID = _uniqueID;
		productID = _productID;
		productUniqueIdentifier = _productUniqueIdentifier;
		lotNumber = _lotNumber;
		
    }
        
}
