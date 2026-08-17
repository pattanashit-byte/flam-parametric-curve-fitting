# FLAM Assignment — Curve Parameter Estimation

## Problem

Recover the unknown constants `theta`, `M`, and `X` in:

```text
x(t) = t*cos(theta) - e^(M*|t|) * sin(0.3t) * sin(theta) + X

y(t) = 42 + t*sin(theta) + e^(M*|t|) * sin(0.3t) * cos(theta)
```

given a set of `(x, y)` points sampled for `6 < t < 60`, subject to:

* `0° < theta < 50°`
* `-0.05 < M < 0.05`
* `0 < X < 100`

## Approach

1. **Understand the model.**
   The curve consists of a linear component controlled by `theta`, an oscillatory component `sin(0.3t)` with an exponential envelope `e^(M|t|)`, and a horizontal translation controlled by `X`.

2. **Load the data.**
   The `(x, y)` points are read from `xy_data.csv`. Since the CSV does not contain a `t` column, the points are assumed to correspond to uniformly sampled values of `t` between 6 and 60.

3. **Define the parametric curve.**
   For each candidate set of `theta`, `M`, and `X`, the predicted `(x, y)` coordinates are calculated using the given equations.

4. **Define the L1 error.**
   The L1 distance between the actual and predicted points is calculated as:

   ```text
   L1 = sum(|x_actual - x_predicted|
            + |y_actual - y_predicted|)
   ```

5. **Optimize the parameters.**
   `scipy.optimize.differential_evolution` is used to search the bounded parameter space and find the values of `theta`, `M`, and `X` that minimize the total L1 distance.

6. **Validate the result.**
   The fitted curve is plotted against the input data to visually verify the quality of the fit. The total, mean, and maximum L1 errors are also calculated.

7. **Report the final parameters.**
   The optimized values are provided in both parameter form and the Desmos/LaTeX parametric format.

## Files

* `solve.py` — loads the dataset and performs the parameter optimization.
* `xy_data.csv` — input curve points.
* `requirements.txt` — required Python libraries.
* `submission.txt` — final fitted parameter values and equation.
* `fit_plot.png` — fitted curve compared with the input data.
* `README.md` — project documentation.

## Result

```
theta = 0.4888548280 rad  (28.0093184370 deg)
M     = 0.0211688778
X     = 63.3905353915
```

### Error

```
Total L1        = 69.5945480629
Mean L1         = 0.2319818269
Maximum L1      = 0.7475529551
```

## Desmos / LaTeX Submission

```
\left(t*\cos(0.488855)-e^{0.021169\left|t\right|}\cdot\sin(0.3t)\sin(0.488855)+63.390535,42+t*\sin(0.488855)+e^{0.021169\left|t\right|}\cdot\sin(0.3t)\cos(0.488855)\right)
```

## Requirements

```bash
pip3 install -r requirements.txt
```

Required libraries:

* NumPy
* Pandas
* SciPy
* Matplotlib

## Run

```bash
python3 solve.py
```

The program loads the input data, performs the bounded optimization, calculates the L1 error, prints the estimated parameters, generates the submission equation, and saves the fitted curve plot.

## Final Parameters

The final estimated parameters are:

```text
theta = 28.0093184370°
M     = 0.0211688778
X     = 63.3905353915
```

These values produce a fitted curve with a total L1 distance of:

```text
69.5945480629
```
