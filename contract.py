VRF_PUB_KEY = "adfadfasdfsadfsadf"

def getRoundSeedHash(round_):
  return Sha512_256( Itob(round_) + Block.seed(round_) + "" )

def getVerifiedRandomness(hash_, vrf_proof)
  verified = VrfVerify(hash_, vrf_proof, VRF_PUB_KEY)
  Assert(verified.out[1] == true)
  return Extract(verified.out[0], 0, 32)

def storeRandomness(round_, vrf_proof):
  strHash = getRoundSeedHash(round_)
  strRandomBytes = getVerifiedRandomness(strHash, vrf_proof)
  gput(Itob(round_), strRandomBytes)

