import random
from gmssl import sm3
from hashlib import sha1
import time

#SM3推荐参数：secp256r1
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2



def show_points(p, a, b):
    return [(x, y) for x in range(p) for y in range(p) if (y * y - (x * x * x + a * x + b)) % p == 0]


def GCD(a, b):
    if b == 0:
        return a
    else:
        return GCD(b, a % b)


def XGCD(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x, y, d = XGCD(b, a % b)
        return y, (x - (a // b) * y), d


# print(XGCD(6553215,5754840))

def get_inverse(a, b):
    return XGCD(a, b)[0] % b


def pow_mod(a, b, n):
    a = a % n
    ans = 1
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while b != 0:
        if b & 1:
            ans = (ans * a) % n
        b >>= 1
        a = (a * a) % n
    return ans


def get_miller(m):
    while (m % 2 == 0):
        m = m // 2
    return m


def rabin_miller(p):
    if p == 2:
        return True
    elif p % 2 == 0:
        return False
    else:
        m = p - 1
        m = get_miller(m)
        the_pow_mod = pow_mod(2, m, p)
        if the_pow_mod == 1:
            return True
        a = m

        while (a <= p - 1):
            the_pow_mod = the_pow_mod ** 2 % p
            if the_pow_mod == 1:
                return True
            a = a * 2
        return False


# 求最大公约数——用于约分化简
def get_gcd(x, y):
    if y == 0:
        return x
    else:
        return get_gcd(y, x % y)

    # 计算P+Q函数



def get_Qr(n,p):
    # 求勒让德符号
    def Legender(a, p):
        return pow_mod(a, (p - 1) >> 1, p)

    class T:
        p = 0
        d = 0

    w = 0

    def multi_er(a, b, m):
        ans = T()
        ans.p = (a.p * b.p % m + a.d * b.d % m * w % m) % m
        ans.d = (a.p * b.d % m + a.d * b.p % m) % m
        return ans

    def power(a, b, m):
        ans = T()
        ans.p = 1
        ans.d = 0
        while b:
            if b & 1:
                ans = multi_er(ans, a, m);
                b -= 1
            b >>= 1
            a = multi_er(a, a, m)
        return ans
    a=0
    t=0
    while True:
        a=random.randrange(1,p)
        t= a*a-n
        w = t%p
        if Legender(w,p)+1==p:
            break
    tmp=T()
    tmp.p = a
    tmp.d = 1
    ans = power(tmp, (p + 1) >> 1, p)
    return ans.p,p-ans.p

def calculate_p_q(x1, y1, x2, y2, a, b, p):
    flag = 1  # 控制符号位

    # 若P = Q，则k=[(3x1^2+a)/2y1]mod p
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 计算分子
        denominator = 2 * y1  # 计算分母

    # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value

    # 求分母的逆元
    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p

    # 计算x3,y3
    """
        x3≡k^2-x1-x2(mod p)
        y3≡k(x1-x3)-y1(mod p)
    """
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算2P函数
def calculate_2p(p_x, p_y, a, b, p):
    tem_x = p_x
    tem_y = p_y
    p_value = calculate_p_q(tem_x, tem_y, p_x, p_y, a, b, p)
    tem_x = p_value[0]
    tem_y = p_value[1]
    return p_value


# 计算nP函数
def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    p_temp = [0, 0]
    # 这里我们不需要考虑b<0，因为分数没有取模运算
    while n != 0:
        if n & 1:
            if (p_value[0] == "0" and p_value[1] == "0"):
                p_value[0], p_value[1] = p_x, p_y
            else:
                p_value = calculate_p_q(p_value[0], p_value[1], p_x, p_y, a, b, p)
        n >>= 1
        p_temp = calculate_2p(p_x, p_y, a, b, p)
        p_x, p_y = p_temp[0], p_temp[1]
    return p_value

def calculate_Tp(p_x, p_y,a, b, p):
    return p_x,p-p_y






def get_key():
    dA=random.randrange(0,n)
    PA=calculate_np(Gx, Gy, dA, a, b, p)
    return dA,PA

def get_bitsize(num):
    len=0
    while num/256:
        len+=1
        num=int (num/256)
    return len

def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num),byteorder='big', signed=False)
def bytes_to_int(bytes):
    return int.from_bytes(bytes,byteorder='big')

msg="dfq202100460092"

def ECDSA():
    PA=[0,0]
    def ECDSA_sign(msg):
        t1=time.time()
        nonlocal  PA
        M = msg.encode()
        dA, PA = get_key()
        k = random.randrange(1, n)
        R = calculate_np(Gx, Gy, k, a, b, p)
        r = R[0] % n
        e = int(sha1(M).hexdigest(), 16)
        s = (get_inverse(k, n) * (e + dA * r)) % n
        t2=time.time()
        print("待签名的消息为：",msg)
        print("生成的签名为：")
        print(r,s)
        print(PA)
        print(e)
        print("签名用时：",t2-t1,"s")
        return r, s

    def ECDSA_verif_sign(msg, sign):
        t1 = time.time()
        r, s = sign
        M = msg.encode()
        e = int(sha1(M).hexdigest(), 16)
        w = get_inverse(s, n)
        temp1 = calculate_np(Gx, Gy, e * w, a, b, p)
        temp2 = calculate_np(PA[0], PA[1], r * w, a, b, p)
        R, S = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        t2 = time.time()
        if (r == R):
            print("验证成功")
            print("验证用时：", t2 - t1, "s")
            return True

        else:
            return False
    return ECDSA_verif_sign(msg,ECDSA_sign(msg))

P=[26877259512020005462763638353364532382639391845761963173968516804546337027093, 48566944205781153898153509065115980357578581414964392335433501542694784316391]
r,s=41159732757593917641705955129814776632782548295209210156195240041086117167123, 57859546964026281203981084782644312411948733933855404654835874846733002636486
def forge_ECDSA():
    def forge_sign():
        u = random.randrange(1, n)
        v = random.randrange(1, n)
        temp1 = calculate_np(Gx, Gy, u, a, b, p)
        temp2 = calculate_np(P[0], P[1], v, a, b, p)
        R = x, y = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        f_r = x % n
        f_e = (f_r * u * get_inverse(v, n)) % n
        f_s = (f_r * get_inverse(v, n)) % n
        return f_r, f_s, f_e

    r,s,e=forge_sign()

    def verify(r,s,e):
        w = get_inverse(s, n)
        temp1 = calculate_np(Gx, Gy, e * w, a, b, p)
        temp2 = calculate_np(P[0], P[1], r * w, a, b, p)
        R, S = calculate_p_q(temp1[0], temp1[1], temp2[0], temp2[1], a, b, p)
        if (r == R):
            return True
        else:
            return False
    return verify(r,s,e)

print(forge_ECDSA())
print(ECDSA())



#print(verif_sign(msg,sign(msg,IDA),IDA))
