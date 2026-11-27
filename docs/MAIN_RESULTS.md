# Main results and scope

This summary follows Theorem A, Theorem B and Corollary C; consult the manuscript for exact hypotheses and proofs. Full human mathematical review is pending.

Let $r\ge2$ be an integer, $h_r(w)=1-(1-w)^{1/r}$, $y_1=1$, and $y_{n+1}=h_r(ty_n)$. Define the coefficientwise limit

$$
B_r(t)=\lim_{n\to\infty}r^ny_{n+1}(t)/t^n,\qquad
S_r(t)=B_r(t)^{1/r}=\sum_{m\ge0}s_{r,m}t^m.
$$

The manuscript establishes integrality and degree at most $m$ of $(m+1)!R^m b_{R,m}\in\mathbb Z[R]$, where $b_{R,m}=[t^m]B_R$.

## Theorem A — denominator classification

For integers $r\ge2$ and $m\ge0$, the coefficients are nonzero and

$$
\operatorname{den}(s_{r,m})=\prod_{p\mid r}p^{e_p(r,m)}.
$$

For $a=v_p(r)\ge1$:

- $p=2$: $(2a+1)m+v_2(m!)$;
- odd $p$, with $p\ge5$ or $a\ge2$: $2am+v_p(m!)$;
- $p=3,\ a=1,\ m\not\equiv2\pmod3$: $2m+v_3(m!)$;
- $p=3,\ a=1,\ m=3n+2,\ u=r/3$: $\max(0,2m+v_3(m!)-v_3(u-\alpha_n))$.

Here $\alpha_n$ is the unique root in $\mathbb Z_3$ of the explicit polynomial $F_{3n+2}$ of the normal-form theorem, with $\alpha_n\equiv-1\pmod3$. For $u\equiv1\pmod3$ the correction vanishes. The quadratic case recovers $4m-s_2(m)$, with $s_2(m)$ the binary digit sum (OEIS A120738).

## Theorem B — exceptional-root interpolation

The manuscript constructs the unique normalized solution $\rho\in\mathbb Z_3[[x]]$ of its explicit formal equation, with

$$
\rho(3n)=\alpha_n,\quad
\rho(x)=-\frac1{1+x}+3x\chi(x),\quad
\chi\in\mathbb Z_3[[x]],\quad\chi(0)\equiv1\pmod3.
$$

For $j,n\ge1$:

$$
v_3(\Delta^j\alpha_0)=j+v_3(j!),\qquad
v_3\left(\alpha_n+\frac1{1+3n}\right)=2+v_3(n).
$$

See Sections 5–8 for the cumulant filtration, ratio system and finite differences.

## Corollary C — index form

The map $\alpha(z)=\rho(3z)$ bijects $\mathbb Z_3$ with $-1+3\mathbb Z_3$ and scales 3-adic distances by $1/3$. For $\eta=\alpha^{-1}$, the normalized coefficient $W_m(u)=9^m m!s_{3u,m}$ (extended through the coefficient functions) satisfies

$$
v_3(W_{3n+2}(u))=1+v_3(n-\eta(u)),
\quad u\in-1+3\mathbb Z_3,\ n\ge0.
$$

## Scope and prior work

The Koenigs interpretation is classical. Section 6 specializes Kallat's Theorem 12.1 and provides additional family-specific estimates recovering the index law. The integral formal control in coordinates $x=3n,\ v=u+1$ is distinguished from disk interpolation in $z=n,\ w=(u+1)/3$. No impossibility of obtaining the stronger control by another method is asserted. No certified novelty or priority is claimed.
