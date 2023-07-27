# project-10
report on the application of this deduce technique in Ethereum with ECDSA
# ECDSA算法描述
### 算法概述 
ECDSA即椭圆曲线数字签名算法，是使用椭圆曲线密码（ECC）对数字签名算法（DSA）的模拟。ECDSA于1999年成为ANSI标准，并于2000年成为IEEE和NIST标准。

与普通的离散对数问题（discrete logarithm problem DLP）和大数分解问题（integer factorization problem IFP）不同，椭圆曲线离散对数问题（elliptic curve discrete logarithm problem ECDLP）没有亚指数时间的解决方法。因此椭圆曲线密码的单位比特强度要高于其他公钥体制。

椭圆曲线密码体制的安全性基于椭圆曲线离散对数问题（ECDLP）的难解性。椭圆曲线离散对数问题远难于离散对数问题，椭圆曲线密码系统的单位比特强度要远高于传统的离散对数系统。因此在使用较短的密钥的情况下，ECC可以达到于DL系统相同的安全级别。这带来的好处就是计算参数更小，密钥更短，运算速度更快，签名也更加短小。因此椭圆曲线密码尤其适用于处理能力、存储空间、带宽及功耗受限的场合。
### 算法原理
![image](https://github.com/jlwdfq/project-10/assets/129512207/198f9d60-b96b-4f5b-ae7d-2f0ee19b1491)

### ECDSA与区块链关系
1.比特币目前使用的 ECDSA 签名算法与建议的 Schnorr 签名算法，都属于椭圆曲线数字签名算法，它们使用的椭圆曲线都是 secp256k1。

2.ECDSA是基于 ECC 的数字签名算法，在比特币、以太坊等区块链网络中大量使用。每一笔区块链交易执行之前都必须进行权限校验，以确保该交易是由账户对应的私钥签发。256 位私钥的 ECDSA 签名可以达到 3072 位 RSA 签名的安全强度。
### 算法标准
1.ANSI X9.62
该项目始于1995年，并于1999年正式作为ANSI标准颁布。ANSI X9.62具有高安全性和通用性。

2.FIPS 186-2
1997年，NIST开始制定包括椭圆曲线和RSA签名算法的FIPS 186标准。

3、IEEE 1363-2000
该标准于2000年作为IEEE标准问世。IEEE 1363的覆盖面很广，包括公钥加密，密钥协商，基于IFP、DLP、ECDLP的数字签名。它与ANSI X9.62和FIPS 186完全不同，它没有最低安全性限制（比如不再对基点阶进行限制），用户可以有充分的自由。
因此IEEE 1363-2000并不是一个安全标准，也不具有良好的通用性，它的意义在于给各种应用提供参照。它的基域可以是，也可以是。 中的元素可以以多项式形式或正规基形式来表示。中元素表示形式是整数，中元素表示形式是字符串。这与ANSI X9. 62和FIPS 186是一致的。

4.ISO/IEC 14888-3
这个标准包含若干签名算法，其中ECDSA部分与ANSI X9.62一致。
#  算法实现
### 签名算法
CDSA是ECC与DSA的结合，整个签名过程与DSA类似，所不一样的是签名中采取的算法为ECC，最后签名出来的值也是分为r,s。 签名过程如下：

1、选择一条椭圆曲线Ep(a,b)，和基点G；

2、选择私有密钥k（k<n，n为G的阶），利用基点G计算公开密钥K=kG；

3、产生一个随机整数r（r<n），计算点R=rG；

4、将原数据和点R的坐标值x,y作为参数，计算SHA1做为hash，即Hash=SHA1(原数据,x,y)；

5、计算s≡r - Hash * k (mod n)

6、r和s做为签名值，如果r和s其中一个为0，重新从第3步开始执行
```python
def ECDSA():
    PA=[0,0]
    def ECDSA_sign(msg):
        nonlocal  PA
        M = msg.encode()
        dA, PA = get_key()
        k = random.randrange(1, n)
        R = calculate_np(Gx, Gy, k, a, b, p)
        r = R[0] % n
        e = int(sha1(M).hexdigest(), 16)
        s = (get_inverse(k, n) * (e + dA * r)) % n
        print("获得的签名为：")
        print(r,s)
        return r, s
```
### 验证算法
验证过程如下：

1、接受方在收到消息(m)和签名值(r,s)后，进行以下运算

2、计算：sG+H(m)P=(x1,y1), r1≡ x1 mod p。

3、验证等式：r1 ≡ r mod p。

4、如果等式成立，接受签名，否则签名无效。
```python
  def ECDSA_verif_sign(msg, sign):
        r, s = sign
        M = msg.encode()
        e = int(sha1(M).hexdigest(), 16)
        w = get_inverse(s, n)
        temp1 = calculate_np(Gx, Gy, e * w, a, b, p)
        temp2 = calculate_np(PA[0], PA[1], r * w, a, b, p)
        R, S = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        if (r == R):
            print("结果正确")
            return True
        else:
            print("结果错误")
            return False
    return ECDSA_verif_sign(msg,ECDSA_sign(msg))
```
# 实验结果
![image](https://github.com/jlwdfq/project-10/assets/129512207/2880c31e-f46b-4345-adf8-0d618ca7f715)
1.签名算法用时： 0.0508275032043457 s

2.验证算法用时： 0.09291815757751465 s
# 实验环境
| 语言  | 系统      | 平台   | 处理器                     |
|-------|-----------|--------|----------------------------|
| Cpp   | Windows10 | pycharm| Intel(R) Core(TM)i7-11800H |
# 小组分工
戴方奇 202100460092 单人组完成project10
