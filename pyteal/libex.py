from pyteal import *

def ensure_budget(ops):
  opup = OpUp(OpUpMode.OnCall)
  return Seq(opup.ensure_budget(ops))

def asset_bal(addr, asset_index):
  b = AssetHolding.balance(addr, Txn.assets[asset_index])
  return Seq(
     b, 
     If( b.hasValue(), b.value(), Int(0) )
   )

@Subroutine(TealType.anytype)
def ggeti(key) -> Expr:
    maybe = App.globalGetEx(Int(0), key)
    return Seq(maybe, If(maybe.hasValue(), maybe.value(), Int(0)))
    
@Subroutine(TealType.anytype)
def lgeti(key) -> Expr:
    """Returns the result of a local storage MaybeValue if it exists, else return a default value"""
    mv = App.localGetEx(Int(0), Int(0), key)
    return Seq(mv, If(mv.hasValue()).Then(mv.value()).Else(Int(0)))

@Subroutine(TealType.bytes)
def ggets(key) -> Expr:
    maybe = App.globalGetEx(Int(0), key)
    return Seq(maybe, If(maybe.hasValue(), maybe.value(), Bytes("")))
    
@Subroutine(TealType.bytes)
def lgets(key) -> Expr:
    """Returns the result of a local storage MaybeValue if it exists, else return a default value"""
    mv = App.localGetEx(Int(0), Int(0), key)
    return Seq(mv, If(mv.hasValue()).Then(mv.value()).Else(Bytes("")))

