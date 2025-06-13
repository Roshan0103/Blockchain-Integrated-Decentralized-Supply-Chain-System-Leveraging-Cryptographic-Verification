pragma solidity >=0.4.22 <0.9.0;
    contract ProductContract {
    string public productID;
	
    
    function perform_transactions(string memory _productID) public{
       productID = _productID;
		
    }
        
}
