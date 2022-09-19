from libex import *

VRF_PUB_KEY = Addr("VLIGLVC4GXW6JLRWZZVKKXAHSGBZ5AOVKC5WTANMZQTXVIJMSBTNBUE7TY")


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
  gput('round', Itob(round_))
  gput('randbytes', strRandomBytes)
  #gput(Itob(round_), strRandomBytes)

@bytes
def userRandom(userAddr):
  strRound = ggets('round')
  return Sha3_256( "" + ggets('randbytes') + strRound + userAddr)

def creatorOnly():
  _creator_ = AppParam.creator(0)
  _creator_
  #Assert( Txn.sender == _creator_.value() )

def app():
  creatorOnly()

  if args_[0] == 'store':
    round_ = Btoi(args_[1])
    strVrfProof = args_[2]
    ensure_budget(7000)
    storeRandomness(round_, strVrfProof)
  
  if args_[0] == 'get':
    #round_ = Btoi(args_[1])
    strAddress = args_[1]
    print(userRandom(strAddress))

  return 1

