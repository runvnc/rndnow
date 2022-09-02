from libex import *

VRF_PUB_KEY = "SJBLLZUWHP6FP27NK47CRZM33ANIDNPUWZIAB3ZGMPD4GEIBHKVVPXMVBQ"

@bytes
def getRoundSeedHash(round_):
  return Sha512_256( Itob(round_) + Block.seed(round_) + "" )

@bytes
def getVerifiedRandomness(hash_, vrf_proof):
  _verified_ = VrfVerify(hash_, vrf_proof, VRF_PUB_KEY)
  _verified_
  Assert(_verified_.out[1] == 1)
  return Extract(_verified_.out[0], 0, 32)

def storeRandomness(round_, vrf_proof):
  strHash = getRoundSeedHash(round_)
  strRandomBytes = getVerifiedRandomness(strHash, vrf_proof)
  gput(Itob(round_), strRandomBytes)

@bytes
def userRandom(strRound, userAddr):
  return Sha3_256( "" + ggets(strRound) + strRound + userAddr)

def creatorOnly():
  _creator_ = AppParam.creator(0)
  _creator_
  Assert( Txn.sender == _creator_.value() )
 

def app():
  creatorOnly()

  if args_[0] == 'store':
    strRound = args_[1]
    strVrfProof = args_[2]
    storeRandomness(strRound, strVrfProof)
  
  if args_[0] == 'get':
    strRound = args_[1]
    print(userRandom(strRound, Txn.accounts[1]))

  return 1

