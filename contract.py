VRF_PUB_KEY = "adfadfasdfsadfsadf"

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
  return 1

def app():
  return storeRandomness(2345234544, args_[1])

