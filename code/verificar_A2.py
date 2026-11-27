#!/usr/bin/env python3
"""A2 -- exact checks backing the tables and the finite certificate of manuscript_A.tex.
Version v0.9.0 (A3-2, 2026-11-24): interface restricted to the default configuration (R08),
infinite tail truncation documented and checked (R09), comparison sources documented (R15).
Mathematical computations are unchanged with respect to A2 v0.8.0.

Standard library only (fractions, math).  Run:  python3 -I -B verificar_A2.py > verificar_A2.log

Supported configuration (the only one): MB=26 (moment/beta order), L=10 (ratio system modulo
m^L), K=20 (Hensel precision 3^K, internal).  These are the values behind the tables of
Section 9.  The script takes no arguments; for backward compatibility it also accepts exactly
"26" or "26 10".  Any other argument list is rejected with exit code 2 before any computation.
Other values would require new precision/length checks (historical vectors hist15, cl10, p8
have fixed lengths; chi(0) needs precision >= 9 on rho_1; the tail needs kappa up to q_max+1)
and are deliberately not supported.
Nothing here proves an all-index statement; the only deductive step is the rational
certificate s_{6,5} (Section [C]), which the manuscript uses together with proved theorems.

Independence: this script does not import any A1 or historical script.  B_r is computed by the
product formula B = prod P_r(t y_i) (not by the B_{n+1} recurrence), S_r by the binomial series
(1+X)^{1/r} (not by r B S' = B' S); beta_m(R) by exact interpolation (degree <= m is a theorem,
and extra nodes are checked); kappa_m(u), W_m(u) symbolically over Q[u,1/u]; the ratio system is
solved in Z_3[[x,v]]/m^L with m=(3,x,v), v=u+1.
"""
from fractions import Fraction as F
from math import factorial, comb
import sys, time

MB_DEFAULT, L_DEFAULT = 26, 10
USAGE = ('usage: python3 -I -B verificar_A2.py   (no arguments; only the default configuration '
         'MB=26, L=10, K=20 is supported; "26" or "26 10" are accepted as explicit defaults)')
_args = sys.argv[1:]
if _args not in ([], ['26'], ['26', '10']):
    print('verificar_A2.py: unsupported arguments ' + repr(_args) + '.', file=sys.stderr)
    print(USAGE, file=sys.stderr)
    sys.exit(2)   # usage error, not a mathematical failure

T0 = time.time()
FAIL = []
def check(cond, label):
    if not cond:
        FAIL.append(label); print('  FAIL:', label)

def v_p(q, p):
    q = F(q)
    if q == 0: return float('inf')
    a, n, d = 0, abs(q.numerator), q.denominator
    while n % p == 0: n //= p; a += 1
    while d % p == 0: d //= p; a -= 1
    return a

def den_exp(q, p):
    """exponent of p in the reduced denominator of q (den(0)=1)."""
    q = F(q); d = q.denominator; e = 0
    while d % p == 0: d //= p; e += 1
    return e

# ---------------------------------------------------------------- [A] numeric coefficients
def ser_mul(a, b, M):
    out = [F(0)] * (M + 1)
    for i, ai in enumerate(a[:M + 1]):
        if ai:
            for j, bj in enumerate(b[:M + 1 - i]):
                if bj: out[i + j] += ai * bj
    return out

def coeffs_product(r, M):
    """b_{r,m}, s_{r,m} (m<=M) via B=prod_{i=1}^{M} P_r(t y_i), S=(1+X)^{1/r} binomially."""
    r = F(r)
    c = [F(1)]  # coefficients of P_r(w): c_j = lambda_{j+1}(r)/(r^j (j+1)!)
    for j in range(1, M + 1):
        c.append(c[-1] * (j * r - 1) / (r * (j + 1)))
    y = [F(1)] + [F(0)] * M          # y_1 = 1
    B = [F(1)] + [F(0)] * M
    for i in range(1, M + 1):
        w = [F(0)] + y[:M]           # w = t*y_i
        # P_r(w) by Horner
        P = [F(0)] * (M + 1)
        for cj in reversed(c):
            P = ser_mul(P, w, M); P[0] += cj
        B = ser_mul(B, P, M)
        y = ser_mul([F(0), 1 / r] + [F(0)] * (M - 1), ser_mul(y, P, M), M)  # y_{i+1}=(t/r) y_i P
    X = [F(0)] + B[1:]
    S = [F(1)] + [F(0)] * M; Xk = [F(1)] + [F(0)] * M; binom = F(1)
    for k in range(1, M + 1):
        binom = binom * (1 / r - (k - 1)) / k
        Xk = ser_mul(Xk, X, M)
        S = [s + binom * xk for s, xk in zip(S, Xk)]
    return B, S

print('[A] product formula and binomial root; S^r = B for small integer r')
for r in [2, 3, 6]:
    B, S = coeffs_product(r, 8)
    Sr = [F(1)] + [F(0)] * 8
    for _ in range(r): Sr = ser_mul(Sr, S, 8)
    check(Sr == B, f'S^r=B r={r}')
B, S = coeffs_product(F(7, 3), 4)   # non-integer R: formulas of Prop. first coefficients are identities in R
R = F(7, 3)
check(B[1] == (R - 1) / (2 * R) and B[2] == (R * R - 1) / (3 * R * R) and B[3] == (R * R - 1) * (6 * R + 1) / (24 * R ** 3), 'b1,b2,b3 at R=7/3')
check(S[1] == (R - 1) / (2 * R * R) and S[2] == (R - 1) * (R + 3) * (5 * R - 1) / (24 * R ** 4), 's1,s2 at R=7/3')
print('  b_1,b_2,b_3,s_1,s_2 formulas confirmed at R=7/3 (rational, non-integer)')

# ---------------------------------------------------------------- [B] beta_m(R) in Z[R]
def lagrange(nodes, vals):
    """coefficients (low->high) of the interpolating polynomial."""
    n = len(nodes); coef = [F(0)] * n
    for i, (xi, yi) in enumerate(zip(nodes, vals)):
        basis = [F(1)]; den = F(1)
        for j, xj in enumerate(nodes):
            if j == i: continue
            basis = [F(0)] + basis
            for k in range(len(basis) - 1): basis[k] -= xj * basis[k + 1]
            den *= (xi - xj)
        for k in range(n): coef[k] += yi * basis[k] / den
    return coef

def peval(p, x):
    s = F(0)
    for c in reversed(p): s = s * x + c
    return s

MB = MB_DEFAULT   # fixed (R08); see module docstring
print(f'[B] beta_m(R)=(m+1)! R^m b_(R,m) for m<={MB}: interpolation on m+1 nodes, checked on 3 extra nodes')
nodes_all = [F(k) for k in range(2, MB + 6)] + [F(-1), F(1, 2), F(-5, 3)]
bvals = {}
for r in nodes_all:
    Bn, _ = coeffs_product(r, MB)
    bvals[r] = Bn
BETA = []
for m in range(MB + 1):
    nodes = nodes_all[:m + 1]
    vals = [factorial(m + 1) * r ** m * bvals[r][m] for r in nodes]
    p = lagrange(nodes, vals)
    while len(p) > 1 and p[-1] == 0: p.pop()
    for r in nodes_all[m + 1:]:
        check(peval(p, r) == factorial(m + 1) * r ** m * bvals[r][m], f'beta_{m} extra node {r}')
    check(all(c.denominator == 1 for c in p), f'beta_{m} integral')
    check(len(p) - 1 <= m, f'deg beta_{m} <= m')
    BETA.append([int(c) for c in p])
for m in range(7):
    print(f'  beta_{m}(R) =', ' + '.join(f'{c}*R^{k}' for k, c in enumerate(BETA[m]) if c))
check(BETA[1] == [-1, 1] and BETA[2] == [-2, 0, 2], 'beta_1, beta_2')
check(BETA[3] == [-1, -6, 1, 6], 'beta_3 = (R^2-1)(6R+1)')
print('  all integral, deg <= m, consistent on extra nodes (incl. R=-1, 1/2, -5/3)')

# ---------------------------------------------------------------- [C] certificate r=6
print('[C] finite certificate r=6 (Theorem: pointwise law)')
B6, S6 = coeffs_product(6, 5)
for m in range(6):
    print(f'  m={m}: beta_m(6)={BETA[m] and int(peval([F(c) for c in BETA[m]], 6))}, b_(6,m)={B6[m]}, s_(6,m)={S6[m]}')
check(S6[5] == F(24199859, 2 ** 18 * 3 ** 8), 's_{6,5}')
W52 = 9 ** 5 * factorial(5) * S6[5]
check(W52 == F(3266980965, 32768) and v_p(W52, 3) == 3, 'W_5(2) and v_3=3')
# s recurrence from r B S' = B' S reproduces the same table (second extraction route)
s_alt = [F(1)]
for m in range(1, 6):
    s_alt.append(sum((F(i, 6) - (m - i)) * B6[i] * s_alt[m - i] for i in range(1, m + 1)) / m)
check(s_alt == S6, 's via r B S\'=B\' S')
print('  W_5(2) =', W52, ' v_3 =', v_p(W52, 3), ' => v_3(2-alpha_1)=3, alpha_1 = 2 mod 27')
inv4 = pow(4, -1, 27)
check((-inv4) % 27 == 20 and (2 - 20) % 27 == 9, 'gamma_1 = 20 mod 27')

# ---------------------------------------------------------------- [D] Laurent polynomials in u
class Lau:
    __slots__ = ('c',)
    def __init__(self, c=None): self.c = {e: F(v) for e, v in (c or {}).items() if v != 0}
    def __add__(s, o):
        o = o if isinstance(o, Lau) else Lau({0: o}); d = dict(s.c)
        for e, v in o.c.items(): d[e] = d.get(e, 0) + v
        return Lau(d)
    __radd__ = __add__
    def __neg__(s): return Lau({e: -v for e, v in s.c.items()})
    def __sub__(s, o): return s + (-(o if isinstance(o, Lau) else Lau({0: o})))
    def __mul__(s, o):
        if not isinstance(o, Lau): return Lau({e: v * o for e, v in s.c.items()})
        d = {}
        for e1, v1 in s.c.items():
            for e2, v2 in o.c.items(): d[e1 + e2] = d.get(e1 + e2, 0) + v1 * v2
        return Lau(d)
    __rmul__ = __mul__
    def shift(s, k): return Lau({e + k: v for e, v in s.c.items()})
    def ev(s, u): u = F(u); return sum((v * u ** e for e, v in s.c.items()), F(0))
    def gauss(s, p=3): return min((v_p(v, p) for v in s.c.values()), default=float('inf'))
    def evmod(s, u, K):
        M = 3 ** K; tot = 0
        for e, v in s.c.items():
            assert v.denominator % 3 != 0
            tot += v.numerator * pow(v.denominator, -1, M) * pow(u, e, M)
        return tot % M
    def deriv(s): return Lau({e - 1: e * v for e, v in s.c.items() if e != 0})
    def __eq__(s, o): return isinstance(o, Lau) and s.c == o.c

U = Lau({1: 1})
M3 = MB
print(f'[D] symbolic kappa_m(u), W_m(u), F_m(u)=u^(2m) W_m for m<={M3}')
# Y = B_{3u}(9y)-1, ordinary coefficients y_i = 3^i beta_i(3u)/((i+1)! u^i)
Yc = [Lau()]
for i in range(1, M3 + 1):
    bt = Lau({k: F(c) * 3 ** k for k, c in enumerate(BETA[i])})   # beta_i(3u)
    Yc.append((bt * F(3 ** i, factorial(i + 1))).shift(-i))
# log(1+Y)
logc = [Lau() for _ in range(M3 + 1)]
Yq = [Lau({0: 1})] + [Lau() for _ in range(M3)]
for q in range(1, M3 + 1):
    new = [Lau() for _ in range(M3 + 1)]
    for i in range(M3 + 1):
        if not Yq[i].c: continue
        for j in range(1, M3 + 1 - i):
            new[i + j] = new[i + j] + Yq[i] * Yc[j]
    Yq = new
    for m in range(M3 + 1): logc[m] = logc[m] + Yq[m] * F((-1) ** (q - 1), q)
kap = [Lau()] + [(logc[m] * F(factorial(m), 3)).shift(-1) for m in range(1, M3 + 1)]   # m!/(3u) [y^m] log
check(kap[1] == Lau({0: F(3, 2), -1: F(-1, 2)}).shift(-1), 'kappa_1')
k1 = Lau({1: 3, 0: -1}) * F(1, 2); k1 = k1.shift(-2)
k2 = Lau({2: 45, 1: 18, 0: -11}) * F(1, 4); k2 = k2.shift(-3)
k3 = Lau({1: 3, 0: -1}) * Lau({2: 9, 1: 5, 0: 2}) * F(27, 4); k3 = k3.shift(-4)
check(kap[1] == k1 and kap[2] == k2 and kap[3] == k3, 'kappa_1,2,3 closed forms')
for m in range(1, M3 + 1):
    num = kap[m].shift(m + 1)
    check(min(num.c) >= 0 and max(num.c) <= m, f'u^(m+1) kappa_{m} polynomial of degree <= m')
    if m >= 3: check(kap[m].gauss() >= m - 2 - v_p(m, 3), f'filtration kappa_{m}')
def omega(q): return q - 1 - v_p(q + 1, 3) - v_p(factorial(q), 3)
dq = [kap[q + 1] * F(1, factorial(q)) for q in range(M3)]
check(dq[2].gauss() >= 3, 'd_2 in 27A')
for q in range(3, M3):
    check(dq[q].gauss() >= omega(q) >= 1, f'd_{q} in 3^omega A')
print(f'  Gauss valuations of kappa_m, m=3..{M3}:', [kap[m].gauss() for m in range(3, M3 + 1)])
print('  bound m-2-v3(m):                    ', [m - 2 - v_p(m, 3) for m in range(3, M3 + 1)])
print(f'  omega_q, q=3..{M3-1}:', [omega(q) for q in range(3, M3)], ' v3-content of d_q:', [dq[q].gauss() for q in range(3, M3)])
# moments
W = [Lau({0: 1})]
for m in range(M3):
    W.append(sum((kap[q + 1] * comb(m, q) * W[m - q] for q in range(m + 1)), Lau()))
Fm = [W[m].shift(2 * m) for m in range(M3 + 1)]
for m in range(1, M3 + 1):
    check(min(Fm[m].c) >= 0 and max(Fm[m].c) <= 2 * m - 1, f'F_{m} polynomial deg<=2m-1')
    check(Fm[m].gauss() >= 0, f'F_{m} 3-integral')
    red = Fm[m] - Lau({0: 1, 1: comb(m, 2)})
    check(red.gauss() >= 1, f'F_{m} = 1+binom(m,2)u mod 3')
check((W[1] - Lau({0: 1})).gauss() <= 0, 'negative control: W_1 - 1 not in 3A (Laurent)')
check(Fm[2] == Lau({1: 1, 0: 1}) * Lau({1: 3, 0: -1}) * Lau({1: 15, 0: -1}) * F(1, 4), 'F_2 closed form')
for u0 in [1, 2, 4, 5, 7, -1, F(1, 2)]:
    if u0 == -1 or isinstance(u0, F): continue
    _, Su = coeffs_product(3 * u0, 8)
    for m in range(9):
        check(W[m].ev(u0) == 9 ** m * factorial(m) * Su[m], f'W_{m}({u0}) = 9^m m! s')
print('  symbolic W_m matches 9^m m! s_(3u,m) at u=1,2,4,5,7 (m<=8); F_m checks done')
for m in range(6):
    print(f'  F_{m}(u) =', ' + '.join(f'({v})u^{e}' for e, v in sorted(Fm[m].c.items())))

# ---------------------------------------------------------------- [E] Hensel roots
K = 20
def poly_mod(Lp, K):
    M = 3 ** K
    return {e: v.numerator * pow(v.denominator, -1, M) % M for e, v in Lp.c.items()}
def pev(pm, u, M): return sum(c * pow(u, e, M) for e, c in pm.items()) % M
def hensel(Lp, K):
    M = 3 ** K; f = poly_mod(Lp, K); fp = poly_mod(Lp.deriv(), K); u = -1 % M
    for _ in range(K + 2): u = (u - pev(f, u, M) * pow(pev(fp, u, M), -1, M)) % M
    assert pev(f, u, M) == 0
    return u
NA = (M3 - 2) // 3
alpha = [hensel(Fm[3 * n + 2], K) for n in range(NA + 1)]
print(f'[E] alpha_n mod 3^{K} (n<={NA}):', alpha)
# R15 -- historical comparison (consistency check, not an independent proof):
# hist15 = roots alpha_n at the discrete indices n=0..10, mod 3^15, as recorded in an earlier
# phase (comment in A2: "audit_03 table"; the same values appear in
# 2026-11-23/.../v0_3/verificacoes/log_verif_alpha_mahler_v0_3.txt).  Compared on n<=NA=8.
hist15 = [14348906, 9038009, 2510042, 11552579, 12699515, 7375964, 3259187, 4897091, 9135941, 672731, 6584384]   # audit_03 table, mod 3^15
check([a % 3 ** 15 for a in alpha] == hist15[:NA + 1], 'alpha_n vs historical table')
check([a % 729 for a in alpha[:4]] == [728, 596, 95, 116], 'alpha_n mod 729 vs v0.4')   # older table, n<=3, mod 3^6
for n, a in enumerate(alpha):
    check(a % 9 == (3 * n - 1) % 9 and a % 27 == (4 ** n - 2) % 27, f'alpha_{n} mod 9, 27')
# global root uniqueness / unit factor: v3(F(u)) = v3(u-alpha) for sample u in Z_3 (integers)
for n in range(NA + 1):
    f = poly_mod(Fm[3 * n + 2], K)
    for u0 in range(-40, 41):
        val = pev(f, u0 % 3 ** K, 3 ** K); d = (u0 - alpha[n]) % 3 ** K
        vv = min(K, v_p(val, 3)) if val else K; vd = min(K, v_p(d, 3)) if d else K
        check(vv == vd, f'v3(F_(3n+2)(u))=v3(u-alpha_n) n={n} u={u0}')
print(f'  v3(F_(3n+2)(u)) = v3(u-alpha_n) for all integers |u|<=40 (precision 3^{K})')

# ---------------------------------------------------------------- [F] denominators of s_(r,m)
print('[F] reduced denominators vs the classification table (m<=8)')
def predicted(r, m):
    out = {}; rr = r; p = 2
    primes = []
    while rr > 1:
        if rr % p == 0:
            primes.append(p)
            while rr % p == 0: rr //= p
        p += 1
    for p in primes:
        a = v_p(r, p)
        if p == 2: e = (2 * a + 1) * m + v_p(factorial(m), 2)
        elif p >= 5 or a >= 2: e = 2 * a * m + v_p(factorial(m), p)
        else:
            u = r // 3
            if m % 3 != 2: e = 2 * m + v_p(factorial(m), 3)
            else:
                n = (m - 2) // 3; dist = (u - alpha[n]) % 3 ** K
                dv = v_p(dist, 3) if dist else K
                assert dv < K
                e = max(0, 2 * m + v_p(factorial(m), 3) - dv)
        out[p] = e
    return out
rows = []
for r in [2, 3, 4, 6, 9, 12, 15, 18, 24, 30, 42, 105, 726, 1155, 2430]:
    _, Sr_ = coeffs_product(r, 8)
    for m in range(9):
        s = Sr_[m]
        check(s != 0, f's_({r},{m}) != 0')
        pr = predicted(r, m)
        dd = 1
        for p, e in pr.items(): dd *= p ** e
        check(F(s).denominator == dd, f'den s_({r},{m})')
    rows.append((r, Sr_[2], predicted(r, 2)))
for r, s2, pr in rows:
    print(f'  r={r}: s_(r,2)={s2}  denominator exponents {pr}')
_, S726 = coeffs_product(726, 2)
check(v_p(S726[2], 3) == 1 and den_exp(S726[2], 3) == 0, 'r=726 m=2')
print('  r=726, m=2: v_3(s)=+1, exponent of 3 in reduced denominator = 0')
check(Fm[2].ev(-1) == 0, 'negative control alpha_0=-1 (u=-1, r=-3 outside the domain)')

# ---------------------------------------------------------------- [G] ratio system in Z_3[[x,v]]/m^L
L = L_DEFAULT   # fixed (R08); see module docstring
print(f'[G] ratio system in Z_3[[x,v]]/m^{L}, m=(3,x,v), u=-1+v')
MODS = {}
def md(i, k): return 3 ** (L - i - k)
def el(d):  # normalize dict {(i,k):c}
    return {(i, k): c % md(i, k) for (i, k), c in d.items() if i + k < L and c % md(i, k)}
def add(*fs):
    d = {}
    for f in fs:
        for key, c in f.items(): d[key] = d.get(key, 0) + c
    return el(d)
def scal(f, c): return el({k: v * c for k, v in f.items()})
def mul(f, g):
    d = {}
    for (i1, k1), c1 in f.items():
        for (i2, k2), c2 in g.items():
            i, k = i1 + i2, k1 + k2
            if i + k < L: d[(i, k)] = d.get((i, k), 0) + c1 * c2
    return el(d)
ONE = el({(0, 0): 1}); ZERO = {}; X = el({(1, 0): 1})
def shift(f, h):  # f(x-3h, v)
    d = {}
    for (i, k), c in f.items():
        for j in range(i + 1):
            d[(j, k)] = d.get((j, k), 0) + c * comb(i, j) * (-3 * h) ** (i - j)
    return el(d)
def inv(f):
    c0 = f.get((0, 0), 0); assert c0 % 3
    ic = pow(c0, -1, 3 ** L)
    n = add(ONE, scal(f, -ic))            # 1 - f/c0, in (x,v) + 3-adic small? constant term 0
    assert (0, 0) not in n
    s = ONE; p = ONE
    for _ in range(L): p = mul(p, n); s = add(s, p)
    return scal(s, ic)
def lau_to_v(Lp):
    """image of a Laurent polynomial in u under u -> -1+v, as series in v mod m^L."""
    d = {}
    # u^e = (-1+v)^e ; for e<0, (-1+v)^{-1} = -sum v^k
    for e, c in Lp.c.items():
        cm = c.numerator * pow(c.denominator, -1, 3 ** L)
        if e >= 0:
            for k in range(min(e, L - 1) + 1): d[(0, k)] = d.get((0, k), 0) + cm * comb(e, k) * (-1) ** (e - k)
        else:
            E = -e   # (-1+v)^{-E} = (-1)^E (1-v)^{-E} = (-1)^E sum binom(E+k-1,k) v^k
            for k in range(L): d[(0, k)] = d.get((0, k), 0) + cm * (-1) ** E * comb(E + k - 1, k)
    return el(d)
# R09 -- certified truncation of the infinite tails Theta_c = sum_{q>=2} d_q (x+c)_q P_{c-q}.
# The q-th term lies in 3^{omega_q} R (Thm 6.1), with omega_2 := 3 from the exact value
# d_2 = kappa_3/2 in 27A (the general bound gives only 0 at q=2, so q=2 is handled by kappa_3).
# Terms with omega_q >= L vanish modulo m^L.  The kept range is q<=qmax (qmax=18 for L=10).
#   * 19 <= q <= 199: omega_q >= L checked exactly below;
#   * q >= 200: Thm 6.1 gives omega_q >= g(q) = (q-1)/2 - log_3(q+1); g'(q) = 1/2 - 1/((q+1) ln 3)
#     > 0 for q >= 1, so g is increasing, and g(200) > 94 > L.  Hence no term with q >= 200 is
#     needed, and the truncation is exact modulo m^L for every q.
import math
qmax = max(q for q in range(2, 200) if (3 if q == 2 else omega(q)) < L)
assert all(omega(q) >= L for q in range(qmax + 1, 200))
_g = lambda q: (q - 1) / 2 - math.log(q + 1, 3)
assert _g(200) > 94 >= L and all(_g(q + 1) > _g(q) for q in range(1, 400))
print(f'  tails truncated at q<={qmax} (omega_q >= {L} beyond, so those terms lie in 3^L R)')
print(f'  tail certificate: q=2 via exact kappa_3 (d_2 in 27A); omega_q>={L} checked for {qmax+1}<=q<=199; '
      f'q>=200: omega_q >= (q-1)/2-log_3(q+1) >= g(200) > 94 (g increasing)')
need = qmax + 1
if need > M3:
    print('  (need kappa up to', need, '- extending symbolic computation)')
assert need <= M3, 'increase M3'
A_ = lau_to_v(kap[1]); B_ = lau_to_v(kap[2])
Dq = {q: lau_to_v(dq[q]) for q in range(2, qmax + 1)}
def falling(c, q):  # (x+c)_q as element
    f = ONE
    for i in range(q): f = mul(f, el({(0, 0): c - i, (1, 0): 1}))
    return f
FALL = {(c, q): falling(c, q) for c in range(3) for q in range(2, qmax + 1)}
def update(Bs, Cs, Ts):
    maxh = (qmax + 2) // 3 + 1
    Bh = [shift(Bs, h) for h in range(maxh + 1)]
    Ch = [shift(Cs, h) for h in range(maxh + 1)]
    Ti = [inv(shift(Ts, h)) for h in range(maxh + 1)]
    prod = [ONE]
    for h in range(1, maxh + 1): prod.append(mul(prod[-1], Ti[h]))
    def P(sig):
        h = (-sig + 2) // 3; i = sig + 3 * h
        return mul([ONE, Bh[h], Ch[h]][i], prod[h])
    Th = []
    for c in range(3):
        acc = ZERO
        for q in range(2, qmax + 1): acc = add(acc, mul(mul(Dq[q], FALL[(c, q)]), P(c - q)))
        Th.append(acc)
    Bn = add(A_, mul(mul(X, B_), mul(Ch[1], Ti[1])), Th[0])
    Cn = add(mul(A_, Bn), mul(add(X, ONE), B_), Th[1])
    Tn = add(mul(A_, Cn), mul(mul(add(X, scal(ONE, 2)), B_), Bn), Th[2])
    return Bn, Cn, Tn
Bs, Cs, Ts = ONE, ZERO, ONE
for it in range(L + 1): Bs, Cs, Ts = update(Bs, Cs, Ts)
check((Bs, Cs, Ts) == update(Bs, Cs, Ts), 'fixed point reached')
# uniqueness from another seed in the admissible class
B2, C2, T2 = add(ONE, X), el({(0, 1): 1, (0, 0): 3}), add(ONE, el({(1, 1): 2}))
for it in range(L + 1): B2, C2, T2 = update(B2, C2, T2)
check((B2, C2, T2) == (Bs, Cs, Ts), 'uniqueness: other seed same fixed point')
print('  fixed point reached from (1,0,1) and from another admissible seed (same limit)')
def evx(f, x0, v0):
    M = 3 ** L
    return sum(c * pow(x0, i, M) * pow(v0, k, M) for (i, k), c in f.items()) % M
# identification with ratios W_{3n+c}/W_{3n}
cnt = 0
for u0 in [-1, 2, 5, 8, -4, 11]:
    v0 = (u0 + 1)
    for n in range(0, (M3 - 3) // 3 + 1):
        Mn = 3 ** L
        w = [W[3 * n + c].evmod(u0 % Mn, L) for c in range(4)]
        ia = pow(w[0], -1, Mn)
        check(evx(Bs, 3 * n, v0) == w[1] * ia % Mn, f'B ident u={u0} n={n}')
        check(evx(Cs, 3 * n, v0) == w[2] * ia % Mn, f'C ident u={u0} n={n}')
        check(evx(Ts, 3 * n, v0) == w[3] * ia % Mn, f'T ident u={u0} n={n}')
        cnt += 3
print(f'  identification (B,C,T)(3n,u+1) = W_(3n+c)/W_(3n) mod 3^{L}: {cnt} checks')
# reduction mod 3: C (1 - x k1 k2 / T) = u^-4 (1 + (1+x) u)
Ubar = lau_to_v(Lau({1: 1}))
lhs = mul(Cs, add(ONE, scal(mul(mul(X, mul(A_, B_)), inv(Ts)), -1)))
rhs = mul(lau_to_v(Lau({-4: 1})), add(ONE, mul(add(ONE, X), Ubar)))
diff = add(lhs, scal(rhs, -1))
check(all(c % 3 == 0 for c in diff.values()), 'reduced equation mod 3')
print('  reduced identity C(1 - x k1 k2/T) = u^-4 (1+(1+x)u) holds mod 3')
c01 = Cs.get((0, 1), 0)
check(c01 % 3 ** (L - 1) == 16 % 3 ** (L - 1), 'dC/dv(0,0)=16')
# root V(x)=rho+1
def compose_C(Vc):
    # C(x,V(x)) in Z_3[[x]]/(3,x)^L, Vc[d] for d=1..L-1
    Vpow = [[1] + [0] * (L - 1)]
    for k in range(1, L):
        prev = Vpow[-1]; nxt = [0] * L
        for i, a in enumerate(prev):
            if a:
                for j in range(1, L - i): nxt[i + j] += a * Vc[j]
        Vpow.append(nxt)
    out = [0] * L
    for (i, k), c in Cs.items():
        for d in range(L - i): out[i + d] += c * Vpow[k][d]
    return [out[d] % 3 ** (L - d) for d in range(L)]
Vc = [0] * L
for d in range(1, L):
    Vc[d] = 0
    e = compose_C(Vc)[d]
    Vc[d] = (-e * pow(c01, -1, 3 ** (L - d))) % 3 ** (L - d)
check(all(c == 0 for c in compose_C(Vc)), 'C(x,V(x)) = 0 mod (3,x)^L')
rho = [(-1) % 3 ** L] + [Vc[d] % 3 ** (L - d) for d in range(1, L)]
print(f'  rho mod (3,x)^{L}: coefficient of x^i mod 3^({L}-i):', rho)
# R15 -- comparisons of the same object (coefficients [x^i]rho) with recorded outputs of earlier
# scripts that share definitions and intermediate data (consistency checks, not independent proofs):
# cl10 = A1 (Claude Code) script V5, ratio system mod (3,x)^10, [x^i]rho mod 3^(10-i), i<10
#        (A1/claude_code-opus_5_5-xhigh/verificacoes/v5_rho_sistema_formal_L10.log);
# p8   = vector mod (3,x)^8, [x^i]rho mod 3^(8-i), i<8, from the September 2026 final audit
#        (Atual/.../final_adversarial_audit_mahler.md; also in the A1 V5 L8 log); only the
#        projection of the present L=10 result to precision 3^(8-i) is compared.
cl10 = [59048, 3964, 4880, 1360, 293, 151, 35, 13, 2, 1]       # A1 (Claude) mod 3^(10-i)
p8 = [6560, 1777, 506, 145, 50, 16, 8, 1]                      # final audit (P/Q), mod 3^(8-i)
check(all(rho[i] % 3 ** (L - i) == cl10[i] % 3 ** (L - i) for i in range(L)), 'rho vs A1 table')
check(all(rho[i] % 3 ** (min(L, 8) - i) == p8[i] % 3 ** (min(L, 8) - i) for i in range(min(L, 8))), 'rho vs historical table (mod 3^(8-i))')
for j in range(1, L): check(rho[j] % 3 == (-1) ** (j + 1) % 3, f'a_{j} = (-1)^(j+1) mod 3')
chi0 = ((rho[1] - 1) // 3) % 3
check(chi0 == 1, 'chi(0) = 1 mod 3')
print('  a_j = (-1)^(j+1) mod 3 for j<L; chi(0) = (a_1-1)/3 = 1 mod 3; agrees with A1 and historical tables')
def alpha_of(z):  # alpha(z)=rho(3z) mod 3^L
    M = 3 ** L
    return sum(rho[k] * 3 ** k * pow(z, k, M) for k in range(L)) % M
for n in range(NA + 1):
    check(alpha_of(n) == alpha[n] % 3 ** L, f'rho(3n)=alpha_n n={n}')
print(f'  rho(3n) = alpha_n mod 3^{L} for n<={NA}')

# ---------------------------------------------------------------- [H] Mahler, pointwise, isometry
print('[H] Mahler law, pointwise law, isometry (finite ranges)')
Mk = 3 ** K
for j in range(1, NA + 1):
    d = sum((-1) ** (j - i) * comb(j, i) * alpha[i] for i in range(j + 1)) % Mk
    w = j + v_p(factorial(j), 3)
    check(v_p(d, 3) == w, f'v3(Delta^{j} alpha_0)')
    res = (d // 3 ** w) * pow(factorial(j) // 3 ** v_p(factorial(j), 3), -1, 3) % 3
    check(res == (-1) ** (j + 1) % 3, f'Mahler residue j={j}')
for n in range(1, NA + 1):
    g = (-pow(1 + 3 * n, -1, Mk)) % Mk
    check(v_p((alpha[n] - g) % Mk, 3) == 2 + v_p(n, 3), f'pointwise n={n}')
    Wg = W[3 * n + 2].ev(F(-1, 1 + 3 * n))
    check(v_p(Wg, 3) == 2 + v_p(n, 3), f'v3 W(gamma_n) n={n}')
check(W[2].ev(-1) == 0, 'W_2(gamma_0)=0')
print(f'  Mahler valuations/residues j<={NA}; v3(alpha_n-gamma_n)=v3(W(gamma_n))=2+v3(n), 1<=n<={NA}')
# isometry v3(alpha(z)-alpha(w)) = 1 + v3(z-w)
for z in range(27):
    for w in range(27):
        if z != w and 1 + v_p(z - w, 3) < L:
            check(v_p((alpha_of(z) - alpha_of(w)) % 3 ** L, 3) == 1 + v_p(z - w, 3), f'isometry {z},{w}')
# bijection z -> (alpha(z)+1)/3 on Z/3^(L-1)
Mm = 3 ** (L - 1)
img = sorted(((alpha_of(z) + 1) // 3) % Mm for z in range(Mm))
check(img == list(range(Mm)), 'bijection mod 3^(L-1)')
eta = {}
for z in range(Mm): eta[((alpha_of(z) + 1) // 3) % Mm] = z
for u0 in [2, 5, 8, 11, 14, 17, 26, -4]:
    e = eta[((u0 + 1) // 3) % Mm]          # eta(u0) mod 3^(L-1)
    for n in range(NA + 1):
        val = W[3 * n + 2].evmod(u0 % Mk, K)
        vW = v_p(val, 3) if val else K
        dn = (n - e) % Mm
        pred = 1 + (v_p(dn, 3) if dn else L - 1)
        if pred < L: check(vW == pred, f'U15 v3(W_(3n+2)(u))=1+v3(n-eta(u)) u={u0} n={n}')
print('  isometry on 0<=z,w<27; bijection mod 3^(L-1); U15 deficit law for 8 parameters, n<=%d' % NA)

# ---------------------------------------------------------------- [I] raw moments vs ratios (u=-1)
print('[I] raw exceptional moments at u=-1 are not in the weighted class; the ratios are (n<=3, mod 243)')
M243 = 243
raw = [W[3 * n + 2].evmod(-1 % M243, 5) for n in range(4)]
rat = [W[3 * n + 2].evmod(-1 % M243, 5) * pow(W[3 * n].evmod(-1 % M243, 5), -1, M243) % M243 for n in range(4)]
d3raw = (raw[3] - 3 * raw[2] + 3 * raw[1] - raw[0]) % M243
d3rat = (rat[3] - 3 * rat[2] + 3 * rat[1] - rat[0]) % M243
print('  W_(3n+2)(-1) mod 243:', raw, ' Delta^3 =', d3raw, ' v3 =', v_p(d3raw, 3))
print('  W_(3n+2)/W_(3n) at u=-1 mod 243:', rat, ' Delta^3 =', d3rat, ' v3 =', v_p(d3rat, 3))
check(raw == [0, 204, 156, 72] and v_p(d3raw, 3) == 3, 'raw moments counterexample (weight 4 violated)')
check(rat == [0, 195, 84, 72] and v_p(d3rat, 3) == 4, 'normalized ratios')
print(f'  alpha_n mod 3^10 (n<={NA}):', [a % 3 ** 10 for a in alpha])
print('  gamma_n mod 3^10:', [(-pow(1 + 3 * n, -1, 3 ** 10)) % 3 ** 10 for n in range(NA + 1)])

print()
print('TOTAL FAILURES:', len(FAIL))
print(f'[time {time.time() - T0:.1f}s]')
sys.exit(1 if FAIL else 0)
