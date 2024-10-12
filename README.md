## ECC

ECC is an extremely ingenious **asymmetric** encryption algorithm that perfectly utilizes the **irreversible** nature of elliptic curve geometric addition. It offers advantages such as small key sizes and fast computation speed, making it widely used in various blockchain applications authentication processes.

## TODO

ecc.py 是一个ecc加密在小参数下的简单实现，在现实应用中，模数 p 应取256位（比特币和以太坊等区块链系统都使用256位的椭圆曲线），我们现在的计算性能只能使用个位数数位的p

对于该数量级的椭圆曲线参数，应该很容易用暴力求解，pohlig_hellman.py中是一个简单的离散对数攻击方法，在椭圆曲线参数已知的情况下，获得public key可以求解private key

接下来要想办法实现更大更复杂的参数和私钥，以及实现更多求解方法