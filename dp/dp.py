# dp.py - DP reference voting under a spoofed DGPS, and the drift it causes.
import numpy as np

DT = 1.0
KP, KD = 0.02, 0.28
NOISE = 0.05
DEV_LIMIT = 5.0
JUMP_LIMIT = 1.0


def run(spoof_rate=0.0, refs=3, fusion="median", seconds=600, seed=3):
    rng = np.random.default_rng(seed)
    x = v = 0.0
    trace, prev, dev_alarm, jump_alarm, off = [], None, None, None, None
    max_jump = 0.0
    for t in range(seconds):
        sensors = [x + rng.normal(0, NOISE),
                   x + rng.normal(0, NOISE),
                   x + rng.normal(0, NOISE)][:refs]
        sensors[0] += spoof_rate * t              # DGPS is reference 0
        fused = float(np.median(sensors)) if fusion == "median" else float(np.mean(sensors))
        dev = max(abs(s - fused) for s in sensors)
        jump = 0.0 if prev is None else abs(sensors[0] - prev)
        max_jump = max(max_jump, jump)
        prev = sensors[0]
        if dev > DEV_LIMIT and dev_alarm is None:
            dev_alarm = t
        if jump > JUMP_LIMIT and jump_alarm is None:
            jump_alarm = t
        v += (-KP * (fused - 0.0) - KD * v) * DT
        x += v * DT
        trace.append(x)
        if abs(x) > 20.0 and off is None:
            off = t
    return {"trace": np.array(trace), "dev": dev_alarm, "jump": jump_alarm,
            "off": off, "max_jump": max_jump}


def row(label, r):
    print(f"{label:<36} max_excursion_m {np.abs(r['trace']).max():8.2f} "
          f"final_m {r['trace'][-1]:8.2f} dev_alarm_s {str(r['dev']):>5} "
          f"off_station_s {str(r['off']):>5}")


if __name__ == "__main__":
    print(f"dt {DT:g}s kp {KP:g} kd {KD:g} dev_limit {DEV_LIMIT:g}m jump_limit {JUMP_LIMIT:g}m/sample")
    row("honest, 3 refs, median", run())
    row("spoof 1 m/s, 3 refs, median", run(spoof_rate=1.0))
    row("spoof 1 m/s, 3 refs, mean", run(spoof_rate=1.0, fusion="mean"))
    row("spoof 1 m/s, 2 refs, median", run(spoof_rate=1.0, refs=2))
    slow = run(spoof_rate=0.05)
    row("spoof 0.05 m/s, 3 refs, median", slow)
    print(f"slow ramp: max per-sample jump {slow['max_jump']:.3f} m "
<<<<<<< HEAD
          f"-> jump monitor (limit {JUMP_LIMIT:g}) {'fires' if slow['jump'] is not None else 'silent'}")
=======
          f"-> jump monitor (limit {JUMP_LIMIT:g}) {'fires' if slow['jump'] is not None else 'silent'}")
>>>>>>> d160e37 (Add toolkit files)
