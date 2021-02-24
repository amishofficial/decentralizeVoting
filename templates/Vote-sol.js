pragma solidity ^0.4.18;

contract Voting {
    
    event AddVote(uint candidateID);

    struct Voter {
        bytes32 uid; 
        bytes32 signature;
        // uint candidateVote;
    }
    struct Candidate {
        bytes32 name;
        bytes32 party; 
        bool doesExist; 
    }

    //uint numCandidates; 
    //uint numVoters;
    uint balance

    mapping (uint => sender) Voter;
    mapping (uint => Vote) vote;
    
    //adding candidate
    function addCandidate(bytes32 name, bytes32 uid, bytes32 signature) public {
         if (verify_vote(vote, balance) == true){
            uint candidateID = numCandidates++;
            candidates[candidateID] = Candidate(name,party,true);
            AddVote(candidateID);
         }
    }
    //verification funtion
    function verify_vote(bytes32 vote, uint balance) public {
        if (candidates[candidateID].doesExist == true) {
            uint voterID = numVoters++; //voterID is the return variable
            voters[voterID] = Voter(uid,candidateID);
            return true;
        }
    }
    

    function totalVotes(uint candidateID) view public returns (uint) {
        uint numOfVotes = 0; // we will return this
        for (uint i = 0; i < numVoters; i++) {
            if (voters[i].candidateIDVote == candidateID) {
                numOfVotes++;
            }
        }
        return numOfVotes; 
    }

    function mineVotes() public {
        // candidateID is the return variable
         if (verify_vote(vote, balance) == true){
            uint candidateID = numCandidates++;
            if (numCandidates == 3){
                mineBlock = true
            }
            return mineBlock;
         }
    }
}
