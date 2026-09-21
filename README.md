# scikit-learn template

Provisioned from [`Qode-Platform/fleet-template-v1`](https://github.com/Qode-Platform/fleet-template-v1) — the fleet
lifecycle contract (`bin/`, `fleet.conf`, deploy workflows) with a
scikit-learn starter laid on top.

## Origin

    hand-written (library, no generator) — one Pipeline, no CV leakage

Generated 2026-09-21 on Node v22.12.0 / Python 3.12.3. **Dependencies were
never installed and this has never been built or run.** Boot it once before
trusting it.

## Fleet lifecycle

`fleet.conf` drives every script in `bin/`:

| step | command |
|---|---|
| install | `python3 -m venv .venv && .venv/bin/pip install --upgrade pip -r requirements.txt` |
| build | `(none)` |
| start | `(none — not a service)` |

    ./bin/run       # install, build, start in the foreground
    ./bin/start     # start from existing build artifacts
    ./bin/restart   # rebuild and restart
    ./bin/stop      # stop whatever holds the port

**This repo is not a service.** `START_CMD` is empty, so `./bin/run` will
install and then stop at the start step with the template's own error. That
is intentional — there is nothing to listen on `$PORT`.

## What differs from stock output

- NOT A SERVICE: START_CMD is empty by design; bin/run will stop at the start step.
- Train with: .venv/bin/python -m src.train data/train.csv

---

# scikit-learn scaffold

Hand-written — scikit-learn ships no generator. The point of the layout: all
preprocessing lives inside the `Pipeline`, so cross-validation and the holdout
split never see fitted statistics from the other side.

    python -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt
    python -m src.train data/train.csv
    python -m src.predict artifacts/model.joblib data/new.csv
    pytest

Expects a CSV with `age, income, region, plan, churned`. `OneHotEncoder` is set
to `handle_unknown="ignore"` so unseen categories score instead of raising.
