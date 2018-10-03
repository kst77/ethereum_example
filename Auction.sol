pragma solidity ^0.4.17;
contract Auction {
    
    // Data
    //Structure to hold details of the item
    struct Item {
        uint itemId; // id of the item
        uint[] itemTokens;  //tokens bid in favor of the item
       
    }
    
   //Structure to hold the details of a persons
    struct Person {
        uint remainingTokens; // tokens remaining with bidder
        uint personId; // it serves as tokenId as well
        address addr;//address of the bidder
    }
 
    mapping(address => Person) tokenDetails; //address to person 
    //Person [4] bidders;//Array containing 4 person objects
    Person[] bidders;//Array containing 4 person objects
    
    //Item [3] public items;//Array containing 3 item objects
    Item[] public items;//Array containing 3 item objects
    //address[3] public winners;//Array for address of winners
    address[] public winners;//Array for address of winners
    address public beneficiary;//owner of the smart contract
    

    event BidEvent(address addr, uint itemId, uint count, uint balance);
    
    //functions

    constructor () public payable{    //constructor
		beneficiary = msg.sender;
    }
    
   modifier onlyOwner  {
	  require(msg.sender == beneficiary);
      _;
    }
    
    function fillitems(uint _itemCount)  public payable onlyOwner{
        
        winners.length = 0;
        items.length   = 0;
        
        uint[] memory emptyArray;
       
        for(uint i = 0; i <_itemCount; i++) {
            items.push(Item({itemId:i,itemTokens:emptyArray}));
        }

    }        
    

    function register(address _addr_bidder, uint _remainingTokens) public payable onlyOwner{
        
        uint bidderCount = bidders.length;
        
        for (uint id = 0; id < bidderCount; id++) {
            if (bidders[id].addr == _addr_bidder) { revert();} 
        }
        
        bidders.push(Person({remainingTokens:_remainingTokens, personId : bidderCount, addr :  _addr_bidder}));
        tokenDetails[_addr_bidder]=bidders[bidderCount];

    }
    
    
    function transfer(address _addr, uint _count) public payable onlyOwner{
       _addr.transfer(_count); 
    
    }    
    
    
    function kill() public onlyOwner
     { 
         selfdestruct(beneficiary); 
     }
    
    function bid(uint _itemId, uint _count) public payable{
        /*
            Bids tokens to a particular item.
            Arguments:
            _itemId -- uint, id of the item
            _count -- uint, count of tokens to bid for the item
        */
		
		if (_itemId > items.length - 1) {
			revert();
		}
		
		if (tokenDetails[msg.sender].remainingTokens == 0) {
		    revert();
		}
		
		if (tokenDetails[msg.sender].remainingTokens < _count) {
			revert();
		}
       
	    if (msg.value != 100000000000000000) {
	        revert();   
	    }
        
        uint balance = tokenDetails[msg.sender].remainingTokens - _count;
        
        
        tokenDetails[msg.sender].remainingTokens = balance;
        bidders[tokenDetails[msg.sender].personId].remainingTokens = balance;//updating the same balance in bidders map.
        
        Item storage bidItem = items[_itemId];
        for(uint i = 0; i <_count; i++) {
            bidItem.itemTokens.push(tokenDetails[msg.sender].personId);    
        }
        
        emit BidEvent(msg.sender, _itemId, _count, balance);
    }
    
    

    
    
    function revealWinners() public onlyOwner{

        winners.length = 0;
        address addr;
        
        for (uint id = 0; id < items.length; id++) {
            Item storage currentItem=items[id];
            addr = address(0);
            if(currentItem.itemTokens.length != 0){
				// generate random# from block number 
				uint randomIndex = (block.number / currentItem.itemTokens.length)% currentItem.itemTokens.length; 
				// Obtain the winning tokenId

				uint winnerId = currentItem.itemTokens[randomIndex];
          
			    addr =	bidders[winnerId].addr;
                    
            
                
            }
            winners.push(addr);
        }
    } 
    
    function getSender() public returns(address)
    {
        return(msg.sender);
        
    }
    
    function getLenItems() public returns(uint)
    {
        return(items.length);
        
    }

    function getLenWinners() public returns(uint)
    {
        return(winners.length);
        
    }
    
    function getWinner(uint id) public returns(address)
    {
        return(winners[id]);
        
    }
    

  //Miscellaneous methods: Below methods are used to assist Grading. Please DONOT CHANGE THEM.
    function getPersonDetails(uint id) public constant returns(uint,uint,address){
        return (bidders[id].remainingTokens,bidders[id].personId,bidders[id].addr);
    }

}
