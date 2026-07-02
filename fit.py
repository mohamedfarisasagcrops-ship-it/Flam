import numpy as np, pandas as pd
from scipy.optimize import least_squares

df = pd.read_csv('xy_data.csv')
x = df['x'].values
y = df['y'].values

def residuals(params):
    theta, M, X = params
    u = (x - X) * np.cos(theta) + (y - 42) * np.sin(theta)
    v = -(x - X) * np.sin(theta) + (y - 42) * np.cos(theta)
    v_model = np.exp(M * np.abs(u)) * np.sin(0.3 * u)
    return v - v_model

lb = [np.deg2rad(0.001), -0.0499, 0.001]
ub = [np.deg2rad(49.999), 0.0499, 99.999]

best = None
rng = np.random.default_rng(42)
for trial in range(40):
    theta0 = np.deg2rad(rng.uniform(1, 49))
    M0 = rng.uniform(-0.04, 0.04)
    X0 = rng.uniform(1, 99)
    try:
        res = least_squares(residuals, x0=[theta0, M0, X0], bounds=(lb, ub), method='trf', xtol=1e-14, ftol=1e-14, gtol=1e-14)
    except Exception as e:
        continue
    cost = np.sum(res.fun**2)
    if best is None or cost < best[0]:
        best = (cost, res.x)

cost, params = best
theta, M, X = params
print("theta (rad):", theta, " deg:", np.rad2deg(theta))
print("M:", M)
print("X:", X)
print("cost (sum sq resid):", cost)

u = (x - X) * np.cos(theta) + (y - 42) * np.sin(theta)
print("recovered t range:", u.min(), u.max())
