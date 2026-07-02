# AI R&D Assignment — Parametric Curve Fit

## Result

| Variable | Value |
|---|---|
| θ | 30° = π/6 rad ≈ 0.5235987755982988 |
| M | 0.03 |
| X | 55 |

**Desmos submission string:**
```
\left(t*\cos(0.5235987755982988)-e^{0.03\left|t\right|}\cdot\sin(0.3t)\sin(0.5235987755982988)+55,42+t*\sin(0.5235987755982988)+e^{0.03\left|t\right|}\cdot\sin(0.3t)\cos(0.5235987755982988)\right)
```

## Approach

The given equations, once you separate out the constant offsets, are:

```
x - X = t*cos(θ) - e^(M|t|)*sin(0.3t)*sin(θ)
y - 42 = t*sin(θ) + e^(M|t|)*sin(0.3t)*cos(θ)
```

This is a 2D rotation by angle θ of the point `(u, v) = (t, e^(M|t|)*sin(0.3t))`,
translated by `(X, 42)`. Rotation is invertible, so rotating `(x - X, y - 42)`
by `-θ` recovers `(t, e^(M|t|)*sin(0.3t))` exactly — without needing to know
which data row corresponds to which `t` value up front.

This turns a hard "unordered point cloud on an unknown curve" problem into a
standard nonlinear least-squares problem over only 3 parameters:

1. Guess `(θ, M, X)`.
2. Un-rotate every `(x, y)` point to recover a candidate `t` and a candidate
   `v = e^(M|t|)*sin(0.3t)`.
3. Compute the residual between that `v` and the model prediction using the
   recovered `t`.
4. Minimize the sum of squared residuals over all 1500 points using
   `scipy.optimize.least_squares`, with the given bounds
   (0°<θ<50°, -0.05<M<0.05, 0<X<100), using 40 random restarts to avoid
   local minima.

## Validation

- The optimizer converged to essentially machine precision (~1.8e-8 total
  squared residual) at values extremely close to round numbers, which
  strongly suggests those round numbers (θ=30°, M=0.03, X=55) are the true
  generating parameters, with the fit noise coming from floating point /
  minor data rounding.
- Plugging the rounded values back in: max residual across all 1500 points
  is ~4e-5, and the recovered `t` values fall in [6.05, 59.99], matching the
  given range 6 < t < 60.

## Files

- `fit.py` — full fitting script (reads `xy_data.csv`, runs the rotation-based
  least-squares fit, prints the recovered parameters and validation stats).
