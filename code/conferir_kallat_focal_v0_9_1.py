#!/usr/bin/env python3
"""Independent finite check of the Kallat comparison incorporated in v0.9.1.

Written by Claude Code (Opus 5.5), 25/11/2026, for the private draft v0.9.1.
Standard library only; exact rational arithmetic.  Run:  python3 -I -B conferir_kallat_focal_v0_9_1.py

It does NOT reuse the Codex control script or verificar_A2.py.  The moments
W_m(u) are recomputed from the formal iteration of Prop. 2.1 (product formula),
for fixed rational u in D = -1+3Z_3.  The checks are finite controls of the
statements in the comparison paragraph at the end of Section 6; they are not
a proof (the proof is the text).  In particular the coefficientwise claims
over O = Z_3<w> are checked only at sample points.

Checks:
 [M] Euler exponents c_m of F_C, C = {1} u {2*3^j : j>=1}, for m <= 600:
     closed formula, blocks (v_3(c_m)<0), depth 1, efficiency (1+1/2)/m,
     strict dominance of m=3, c_3=-1/3, c_6=1/3, 3 not in C; Euler product
     equals F_C mod y^M.
 [E] log F_C - (1/2) log E_3(y^2) = y - y^2/2; E_3 and E_3(y^2)^(-1/2)
     3-integral mod y^M; product formula for E_3.
 [H] for each sample u: L_u - y + y^2/2 in 3y Z_(3)[[y]];  V in 1+3yZ_(3)[[y]];
     H_u = F_C * V * E_3(y^2)^(-1/2);  h_k = [y^k] H_u (1-y^3)^(-1/3):
     h_2/3 = -w, h_5 = -1 (mod 3), v(h_8)>=0, v(h_6)=-1, v(h_k)>=-N-v_3(N!);
     [y^(3n+c)]H_u = b*_n f_c(n) exactly; f_0(n) unit; the three ratio
     identities; f_2(n)/3 = n - w (mod 3); v_3(W_(3n+2)) = v_3(f_2(n)).
 [I] e(w) mod 27 from the truncated series f_2(z) at z = 0..26 versus
     eta(u) mod 27 obtained from the printed coefficients of rho (Sec. 9.2),
     and v_3(W_(3n+2)(u)) = 1 + v_3(n - e) for the computed n.
"""
from fractions import Fraction as Fr
import sys, time

T0 = time.time()
M = 30          # series precision in y (moments W_m, m < M)
FAIL = []

def v3(x):
    x = Fr(x)
    if x == 0:
        return 10**9
    n, d, v = x.numerator, x.denominator, 0
    while n % 3 == 0:
        n //= 3; v += 1
    while d % 3 == 0:
        d //= 3; v -= 1
    return v

def mod3(x):
    """residue of a 3-integral rational in {0,1,2}"""
    x = Fr(x); assert v3(x) >= 0
    return (x.numerator * pow(x.denominator, -1, 3)) % 3

def modpk(x, k):
    x = Fr(x); assert v3(x) >= 0
    return (x.numerator * pow(x.denominator, -1, 3**k)) % 3**k

def check(cond, msg):
    if not cond:
        FAIL.append(msg)
    return cond

# ---------- series helpers (lists of Fractions, length M) ----------
def mul(a, b, n=M):
    c = [Fr(0)] * n
    for i, ai in enumerate(a[:n]):
        if ai:
            for j in range(0, n - i):
                if b[j]:
                    c[i + j] += ai * b[j]
    return c

def exp_s(a, n=M):
    assert a[0] == 0
    # e' = a' e
    e = [Fr(0)] * n; e[0] = Fr(1)
    for k in range(1, n):
        s = Fr(0)
        for j in range(1, k + 1):
            s += j * a[j] * e[k - j]
        e[k] = s / k
    return e

def log_s(a, n=M):
    assert a[0] == 1
    # l' = a'/a
    l = [Fr(0)] * n
    for k in range(1, n):
        s = k * a[k]
        for j in range(1, k):
            s -= j * l[j] * a[k - j]
        l[k] = s / k
    return l

def power_s(a, alpha, n=M):
    return exp_s([alpha * c for c in log_s(a, n)], n)

def binom_frac(a, k):
    r = Fr(1)
    for i in range(k):
        r = r * (a - i) / (i + 1)
    return r

# ---------- [M] Moebius / Euler exponents ----------
def mobius(n):
    res, p, m = 1, 2, n
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            res = -res
        p += 1
    if m > 1:
        res = -res
    return res

def inC(d):
    if d == 1:
        return True
    if d % 2 or d < 6:
        return False
    e = d // 2
    while e % 3 == 0:
        e //= 3
    return e == 1 and d // 2 > 1

MM = 600
cm = {}
for m in range(1, MM + 1):
    cm[m] = Fr(sum(mobius(m // d) for d in range(1, m + 1) if m % d == 0 and inC(d)), m)
ok = True
for m in range(1, MM + 1):
    a, b = 0, m
    while b % 3 == 0:
        b //= 3; a += 1
    if a == 0:
        pred = mobius(b)
    elif a == 1:
        pred = (mobius(b // 2) if b % 2 == 0 else 0) - mobius(b)
    else:
        pred = 0
    ok &= check(m * cm[m] == pred, f"[M] closed formula fails at m={m}")
blocks = [m for m in range(2, MM + 1) if v3(cm[m]) < 0]
eff = {m: Fr(-v3(cm[m]) * 2 + 1, 2 * m) for m in blocks}     # (j + 1/(p-1))/m, p=3
check(all(-v3(cm[m]) == 1 for m in blocks), "[M] some block has depth != 1")
check(cm[3] == Fr(-1, 3) and cm[6] == Fr(1, 3), "[M] c_3 or c_6 wrong")
check(not inC(3), "[M] 3 in C")
check(eff[3] == Fr(1, 2) and max(eff[m] for m in blocks if m != 3) == Fr(1, 4)
      and eff[6] == Fr(1, 4), "[M] dominance / efficiencies")
check(all(m % 3 == 0 and (m // 3) % 3 != 0 for m in blocks), "[M] block outside a=1")
check(min(m for m in blocks if m != 3) == 6, "[M] second block not 6")
# Euler product vs F_C
FC_log = [Fr(0)] * M
for d in range(1, M):
    if inC(d):
        FC_log[d] = Fr(1, d)
FC = exp_s(FC_log)
EP = [Fr(1)] + [Fr(0)] * (M - 1)
for m in range(1, M):
    if cm[m]:
        fac = [Fr(0)] * M
        for lam in range(0, (M - 1) // m + 1):
            fac[m * lam] = binom_frac(-cm[m], lam) * (-1) ** lam
        EP = mul(EP, fac)
check(EP == FC, "[M] Euler product != F_C")
print(f"[M] c_m for m<={MM}: closed formula OK={ok}; blocks<=60: {[m for m in blocks if m<=60]}")
print(f"    all depths 1; eff(3)=1/2, max other eff = 1/4 (at 6); c_3=-1/3, c_6=1/3; 3 not in C; "
      f"Euler product = F_C mod y^{M}")

# ---------- [E] Artin-Hasse ----------
AH_log = [Fr(0)] * M          # log E_3(s), as series in s
j = 1
while j < M:
    AH_log[j] = Fr(1, j); j *= 3
E3 = exp_s(AH_log)
check(all(v3(c) >= 0 for c in E3), "[E] E_3 not 3-integral")
E3prod = [Fr(1)] + [Fr(0)] * (M - 1)
for d in range(1, M):
    if d % 3 and mobius(d):
        fac = [Fr(0)] * M
        for lam in range(0, (M - 1) // d + 1):
            fac[d * lam] = binom_frac(Fr(-mobius(d), d), lam) * (-1) ** lam  # (1-s^d)^(-mu(d)/d)
        E3prod = mul(E3prod, fac)
check(E3prod == E3, "[E] product formula for E_3")
E3y2_log = [Fr(0)] * M
for i, c in enumerate(AH_log):
    if c and 2 * i < M:
        E3y2_log[2 * i] = c
E3y2_mhalf = exp_s([-c / 2 for c in E3y2_log])
check(all(v3(c) >= 0 for c in E3y2_mhalf), "[E] E_3(y^2)^(-1/2) not 3-integral")
diff = [FC_log[i] - E3y2_log[i] / 2 for i in range(M)]
check(diff == [Fr(0), Fr(1), Fr(-1, 2)] + [Fr(0)] * (M - 3), "[E] log identity")
print(f"[E] log F_C - (1/2)log E_3(y^2) = y - y^2/2; E_3 = prod_(3 not| d)(1-s^d)^(-mu(d)/d); "
      f"E_3 and E_3(y^2)^(-1/2) 3-integral mod y^{M}")

# ---------- [H] the family ----------
def moments(u):
    """H_u(y)=S_{3u}(9y) mod y^M via Prop 2.1 (product formula); returns H coefficients."""
    r = 3 * Fr(u)
    lam = [Fr(1)] * (M + 1)          # lambda_q(r), q>=1 ; lam[q]
    lam[0] = Fr(0)
    for q in range(2, M + 1):
        lam[q] = lam[q - 1] * ((q - 1) * r - 1)
    hq = [Fr(0)] + [lam[q] / (r ** q * fact[q]) for q in range(1, M)]   # h_r(w)
    Pq = [hq[j + 1] * r for j in range(M - 1)] + [Fr(0)]                   # P_r(w)=r h_r(w)/w
    yi = [Fr(1)] + [Fr(0)] * (M - 1)  # y_1
    B = [Fr(1)] + [Fr(0)] * (M - 1)
    for i in range(1, M + 1):
        ty = [Fr(0)] + yi[:M - 1]                 # t*y_i, order >= i
        # P_r(t y_i) and h_r(t y_i)
        Pv = [Fr(0)] * M; Pv[0] = Pq[0]
        hv = [Fr(0)] * M
        pw = [Fr(1)] + [Fr(0)] * (M - 1)
        q = 0
        while True:
            q += 1
            pw = mul(pw, ty)
            if not any(pw):
                break
            for k in range(M):
                if pw[k]:
                    hv[k] += hq[q] * pw[k] if q < M else 0
                    if q < M - 1:
                        Pv[k] += Pq[q] * pw[k]
        B = mul(B, Pv)
        yi = hv
    S = power_s(B, 1 / r)
    return [S[m] * 9 ** m for m in range(M)]

fact = [1]
for i in range(1, 2 * M):
    fact.append(fact[-1] * i)

samples = [Fr(-1), Fr(2), Fr(5), Fr(8), Fr(26), Fr(242), Fr(-4), Fr(-7),
           Fr(1, 2), Fr(-1, 4), Fr(5, 4)]

# printed coefficients of rho (Sec. 9.2): [x^i]rho mod 3^(10-i)
RHO = [59048, 3964, 4880, 1360, 293, 151, 35, 13, 2, 1]
def alpha_mod81(z):
    return sum(RHO[i] * 3 ** i * z ** i for i in range(4)) % 81

def P_t(t, z):
    p = Fr(1)
    for i in range(t):
        p = p * 3 * (z - i) / (-1 + 3 * (z - 1 - i))
    return p

H2 = None
for u in samples:
    assert v3(u + 1) >= 1
    w = (u + 1) / 3
    H = moments(u)
    W = [H[m] * fact[m] for m in range(M)]
    if u == 2:
        check(W[5] == Fr(3266980965, 32768), "[H] W_5(2) differs from Lemma 8.4")
    L = log_s(H)
    Lc = L[:]; Lc[1] -= 1; Lc[2] += Fr(1, 2)
    check(all(v3(c) >= 1 for c in Lc[1:]), f"[H] u={u}: L-y+y^2/2 not in 3yZ_(3)[[y]]")
    V = exp_s(Lc)
    check(V[0] == 1 and all(v3(c) >= 1 for c in V[1:]), f"[H] u={u}: V not in 1+3yZ_(3)[[y]]")
    Tw = mul(V, E3y2_mhalf)
    check(all(v3(c) >= 0 for c in Tw), f"[H] u={u}: twist not integral")
    check(mul(FC, Tw) == H, f"[H] u={u}: H != F_C T")
    h = mul(H, power_s([Fr(1)] + [Fr(0)] * 2 + [Fr(-1)] + [Fr(0)] * (M - 4), Fr(-1, 3)))
    check(mod3(h[2] / 3) == mod3(-w), f"[H] u={u}: h2/3 != -w")
    check(mod3(h[5]) == 2, f"[H] u={u}: h5 != -1")
    check(v3(h[8]) >= 0 and v3(h[6]) == -1, f"[H] u={u}: h8 / h6")
    for k in range(M):
        N = k // 6
        check(v3(h[k]) >= -N - v3(fact[N]), f"[H] u={u}: tail bound at k={k}")
    bstar = lambda n: binom_frac(Fr(n) - 1 - Fr(1, 3), n)
    f = {}
    for c in range(3):
        for n in range((M - 1 - c) // 3 + 1):
            val = sum(h[3 * t + c] * P_t(t, n) for t in range(n + 1))
            f[(c, n)] = val
            check(H[3 * n + c] == bstar(n) * val, f"[H] u={u}: Kallat identity c={c}, n={n}")
            for t in range(3, n + 1):
                check(v3(h[3 * t + c] * P_t(t, n)) >= 2, f"[H] u={u}: term t={t} not in 9Z")
    nmax = (M - 4) // 3
    for n in range(nmax + 1):
        check(v3(f[(0, n)]) == 0, f"[H] u={u}: f0({n}) not a unit")
        check(W[3*n+1] / W[3*n] == (3*n+1) * f[(1, n)] / f[(0, n)], f"[H] ratio 1, u={u}, n={n}")
        check(W[3*n+2] / W[3*n] == (3*n+1)*(3*n+2) * f[(2, n)] / f[(0, n)], f"[H] ratio 2, u={u}, n={n}")
        check(W[3*n+3] / W[3*n] == (3*n+1)*(3*n+2)*(3*n-1) * f[(0, n+1)] / f[(0, n)], f"[H] ratio 3, u={u}, n={n}")
        check(v3(W[3*n+2]) == v3(f[(2, n)]), f"[H] u={u}: v3(W) != v3(f2), n={n}")
        if f[(2, n)] != 0:
            check(v3(f[(2, n)]) >= 1 and mod3(f[(2, n)] / 3) == mod3(n - w), f"[H] u={u}: f2/3 != n-w mod 3, n={n}")
        else:
            check(mod3(n - w) == 0, f"[H] u={u}: zero of f2 off n=w mod 3")
    # [I] e(w) mod 27 from truncated f_2 on z = 0..26 (terms t <= 9: error in 3^4)
    tmax = (M - 3) // 3
    vals = {}
    for z in range(27):
        s = sum(h[3 * t + 2] * P_t(t, Fr(z)) for t in range(tmax + 1))
        vals[z] = modpk(s / 3, 3)          # f_2(z)/3 mod 27, valid since error/3 in 27Z_3
    zeros = [z for z in range(27) if vals[z] == 0]
    check(len(zeros) == 1, f"[I] u={u}: zeros of f_2/3 mod 27: {zeros}")
    e27 = zeros[0] if zeros else None
    eta = [z for z in range(27) if alpha_mod81(z) == modpk(u, 4)]
    check(eta == [e27], f"[I] u={u}: e mod 27 = {e27}, eta mod 27 from rho = {eta}")
    vlist = [v3(W[3*n+2]) for n in range(nmax + 1)]
    for n in range(nmax + 1):
        d = v3(Fr(n - e27))
        if d < 3:
            check(vlist[n] == 1 + d, f"[I] u={u}: index law at n={n}")
        else:
            check(vlist[n] >= 4, f"[I] u={u}: index law (>=) at n={n}")
    print(f"[H] u={str(u):>5}  w={str(w):>5}: h2/3={mod3(h[2]/3)} (-w={mod3(-w)}), h5={mod3(h[5])}, "
          f"v(h6)={v3(h[6])}, v(h8)={v3(h[8])};  e mod 27 = {e27}, eta mod 27 = {eta}; "
          f"v3(W_3n+2), n=0..{nmax}: {[x if x < 10**8 else 'inf' for x in vlist]}")

print(f"[H] checked for {len(samples)} parameters: identity [y^(3n+c)]H = b*_n f_c(n) (3n+c<{M}), "
      f"three ratio identities, f_0 unit, f_2/3 = n-w mod 3, tail terms t>=3 in 9Z_(3)")
print(f"\nTOTAL FAILURES: {len(FAIL)}")
for msg in FAIL[:40]:
    print("  FAIL", msg)
print(f"[time {time.time()-T0:.1f}s]")
sys.exit(1 if FAIL else 0)
