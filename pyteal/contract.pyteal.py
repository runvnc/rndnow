from pyteal import *

globals().update(TealType.__members__)

from libex import *
VRF_PUB_KEY = Addr("VLIGLVC4GXW6JLRWZZVKKXAHSGBZ5AOVKC5WTANMZQTXVIJMSBTNBUE7TY")



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
    	App.globalPut(Bytes('round'), Itob(round_)),
    	App.globalPut(Bytes('randbytes'), strRandomBytes.load()) )


@Subroutine(TealType.bytes)
def userRandom(userAddr):
    strRound = ScratchVar(TealType.bytes)
    return  Seq(
    	strRound.store(ggets(Bytes('round'))),
    	Return( Sha3_256( Concat(Bytes(""),Concat(ggets(Bytes('randbytes')),Concat(strRound.load(),userAddr)))) ) )

@Subroutine(TealType.none)
def creatorOnly():
    _creator_ = AppParam.creator(Int(0))
    return _creator_

def app():
    strAddress = ScratchVar(TealType.bytes)
    strVrfProof = ScratchVar(TealType.bytes)
    round_ = ScratchVar(TealType.uint64)
    return  Seq(
    	creatorOnly(),
    	If( Txn.application_args[0] == Bytes('store'), 
            Seq(
    	       round_.store(Btoi(Txn.application_args[1])),
    	       strVrfProof.store(Txn.application_args[2]),
    	       ensure_budget(Int(7000)),
    	       storeRandomness(round_.load(), strVrfProof.load()) )
       ),
    	If( Txn.application_args[0] == Bytes('get'), 
            Seq(
    	       strAddress.store(Txn.application_args[1]),
    	       Log(userRandom(strAddress.load())) )
       ),
    	If( Txn.application_args[0] == Bytes('clear'), 
            Seq(
    	       App.globalDel(Bytes('round')),
    	       App.globalDel(Bytes('randbytes')) )
       ),
    	Return( Int(1) ) )


if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=7))
