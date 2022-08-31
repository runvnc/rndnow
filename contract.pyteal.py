# genpyteal version 3.1.1
from pyteal import *

globals().update(TealType.__members__)

VRF_PUB_KEY = Bytes("adfadfasdfsadfsadf")


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
@Subroutine(uint64)
def storeRandomness(round_, vrf_proof):
    strRandomBytes = ScratchVar(TealType.bytes)
    strHash = ScratchVar(TealType.bytes)
    return  Seq(
    	strHash.store(getRoundSeedHash(round_)),
    	strRandomBytes.store(getVerifiedRandomness(strHash.load(), vrf_proof)),
    	App.globalPut(Itob(round_), strRandomBytes.load()),
    	Return( Int(1) ) )
def app():
  return ( storeRandomness(Int(2345234544), Txn.application_args[1]) )



if __name__ == "__main__":
    print(compileTeal(app(), mode=Mode.Application, version=7))
