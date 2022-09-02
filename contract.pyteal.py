from pyteal import *

globals().update(TealType.__members__)

from libex import *

VRF_PUB_KEY = Bytes("SJBLLZUWHP6FP27NK47CRZM33ANIDNPUWZIAB3ZGMPD4GEIBHKVVPXMVBQ")



@Subroutine(TealType.bytes)
def getRoundSeedHash(round_):
  return ( Sha512_256( Concat(Itob(round_),Concat(Block.seed(round_),Bytes(""))) ) )



@Subroutine(TealType.bytes)
def getVerifiedRandomness(hash_, vrf_proof):
    _verified_ = VrfVerify.algorand(hash_, vrf_proof, VRF_PUB_KEY)
    return  Seq(
    	_verified_,
    	Assert(_verified_.output_slots[1].load() == Int(1)),
    	Return( Extract(_verified_.output_slots[0].load(), Int(0), Int(32)) ) )

@Subroutine(TealType.none)
def storeRandomness(round_, vrf_proof):
    strRandomBytes = ScratchVar(TealType.bytes)
    strHash = ScratchVar(TealType.bytes)
    return  Seq(
    	strHash.store(getRoundSeedHash(round_)),
    	strRandomBytes.store(getVerifiedRandomness(strHash.load(), vrf_proof)),
    	App.globalPut(Itob(round_), strRandomBytes.load()) )


@Subroutine(TealType.bytes)
def userRandom(strRound, userAddr):
  return ( Sha3_256( Concat(Bytes(""),Concat(ggets(strRound),Concat(strRound,userAddr)))) )


@Subroutine(TealType.none)
def creatorOnly():
    _creator_ = AppParam.creator(Int(0))
    return  Seq(
    	_creator_,
    	Assert( Txn.sender() == _creator_.value() ) )

def app():
    strVrfProof = ScratchVar(TealType.bytes)
    strRound = ScratchVar(TealType.bytes)
    return  Seq(
    	creatorOnly(),
    	If( Txn.application_args[0] == Bytes('store'), 
            Seq(
    	       strRound.store(Txn.application_args[1]),
    	       strVrfProof.store(Txn.application_args[2]),
    	       storeRandomness(strRound.load(), strVrfProof.load()) )
       ),
    	If( Txn.application_args[0] == Bytes('get'), 
            Seq(
    	       strRound.store(Txn.application_args[1]),
    	       Log(userRandom(strRound.load(), Txn.accounts[1])) )
       ),
    	Return( Int(1) ) )


if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=7))
