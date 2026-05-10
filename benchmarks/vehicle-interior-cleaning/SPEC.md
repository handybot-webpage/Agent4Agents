# VIC Benchmark Specification (v0.1)

> Vehicle Interior Cleaning — embodied sweeping and grasping benchmark for mobile manipulators in vehicle cabins. Paper-inspired by [CleanUpBench (arxiv 2508.05543)](https://arxiv.org/abs/2508.05543), domain-shifted to vehicle interiors.

## 1. Robot platform

| Component | Specification |
|---|---|
| Base | Compact wheeled mobile platform (≤0.5 m × 0.5 m footprint) capable of entering through a vehicle door |
| Arm | 6-DoF manipulator, ≥0.7 m reach, payload ≥1 kg |
| End-effector | Two-mode: parallel gripper (grasping) + active sweeping nozzle (sweeping) |
| Sensors | RGBD camera (head-mounted), proprioceptive joint encoders, contact sensors on end-effector |

The robot is *anchored at the door entry* in v0.1; full mobility inside the cabin is v0.3. This simplification is consistent with how real cleaning robots operate (a docking station outside the vehicle).

## 2. Vehicle classes (3)

| Class | Cabin volume | Seats | Cargo area | Notable obstacles |
|---|---|---|---|---|
| `sedan` | ~3.0 m³ | 5 (3 row1 + 2 row2 hidden in v0.1) | trunk separated | dashboard curve, gear shifter, two mirrors |
| `suv` | ~4.5 m³ | 5–7 | open cargo behind row 2 | higher seat backs, larger cup-holder array |
| `hatchback` | ~2.7 m³ | 4–5 | open cargo continuous | rear seatback fold, lower roof |

Each class is procedurally generated as a primitive-mesh approximation in v0.1 (boxes for seats, cylinders for steering wheel, simplified dashboard plane). Real CAD assets are out of scope until the asset-licensing ADR.

## 3. Clutter classes

| Class | Examples | Interaction mode |
|---|---|---|
| `small_debris` | sand grains, food crumbs, leaves | Sweep |
| `medium_object` | toys, drink cups, snack wrappers | Grasp + relocate to bin |
| `liquid_spill` | water/coffee marker on fabric | Spot-clean (wipe motion) |
| `fabric_dust` | dust on seat cushion | Vacuum (sweep variant) |

Each clutter class has visual + physical properties registered in `configs/clutter.yaml`.

## 4. Tasks (4)

### 4.1 `sweep_floor`
Remove all `small_debris` and `fabric_dust` from the floor area into a designated containment bin (placed at the cabin entry).
- **Action set:** sweep gestures, base pose adjustments
- **Episode length:** 300 s wall-clock simulated time
- **Per-episode count:** 30–80 small debris items, 5–15 fabric_dust patches
- **Termination:** all items collected OR time elapsed

### 4.2 `pickup_objects`
Identify and grasp every `medium_object` and deposit into the bin.
- **Action set:** approach, grasp, lift, place
- **Episode length:** 300 s
- **Per-episode count:** 3–8 medium objects placed in seats, footwells, or cup holders
- **Termination:** all objects in bin OR time elapsed

### 4.3 `spot_clean_seat`
Locate visible `liquid_spill` patches on seats and execute a wiping motion across each, until each is reduced below a stain-coverage threshold.
- **Action set:** approach, contact, lateral wipe with controlled normal force
- **Episode length:** 200 s
- **Per-episode count:** 2–4 spills, randomly placed on seat surfaces
- **Termination:** all spills below threshold OR time elapsed

### 4.4 `full_clean` (composite)
A combined episode of 4.1 + 4.2 + 4.3 with all clutter classes present.
- **Episode length:** 600 s
- **Termination:** all sub-task completion criteria met OR time elapsed

## 5. Metrics (5)

All metrics are normalized to [0, 1] except where noted. Reported per episode and aggregated (mean, std) over the episode count.

### 5.1 Task Completion Rate (TCR)
Fraction of clutter items resolved by the end of the episode.
- For sweeping: items collected / items present
- For grasping: items in bin / items present
- For spot-cleaning: spill patches reduced / patches present

### 5.2 Spatial Efficiency (SE)
Coverage proxy: `1 − (redundant_traversal_area / total_swept_area)`. Penalizes back-and-forth over already-cleaned regions. Measured from the recorded end-effector trajectory projected onto the cleaning plane.

### 5.3 Motion Quality (MQ)
Joint-space smoothness, scored as `exp(−mean_jerk / k)` for tunable `k`. High score = smooth trajectory; low score = jerky or chattering. Computed from logged joint position derivatives.

### 5.4 Control Performance (CP)
Wall-clock time efficiency: `1 − (episode_time / max_episode_time)` clamped to [0, 1]. Episodes that finish quickly score higher.

### 5.5 Damage Avoidance (DA)  *(VIC-specific, not in CleanUpBench)*
`1 − min(1, num_damage_collisions / max_allowed)` where `damage_collisions` are robot contacts with `{seat, dashboard, mirror, windshield, steering_wheel}` exceeding a force threshold. `max_allowed = 5` per episode by convention. Soft taps don't count; only collisions above the force threshold.

A composite score `VIC = mean(TCR, SE, MQ, CP, DA)` is reported but not the sole ranking signal — per-metric breakdown is required for any leaderboard submission.

## 6. Splits

| Split | Vehicle classes | Scenes per class | Purpose |
|---|---|---|---|
| `train` | sedan, suv, hatchback | 100 | training (RL or imitation) |
| `eval-known` | sedan, suv, hatchback | 20 | in-distribution evaluation |
| `eval-novel` | sedan, suv, hatchback (+ held-out clutter combos) | 20 | OOD evaluation |

`eval-novel` holds out specific clutter-class × placement-zone combinations from the training distribution — e.g., trains never see liquid spills on the rear seat, but eval-novel does. This tests generalization without changing the vehicle class itself, since the v0.1 procedural generator is too coarse to make a vehicle-class held-out split meaningful.

## 7. Baselines (provided)

### 7.1 `heuristic`
Pre-scripted policy:
1. Sweep entry-region floor with raster pattern
2. Detect medium objects via simulated RGBD; grasp closest, place in bin, repeat
3. For spills: navigate end-effector to detected centroid, perform circular wipe motion
4. Combined: phase 1 → phase 2 → phase 3 sequentially

Implemented in pure Python; runs without Isaac Sim if given a recorded observation trace.

### 7.2 `map-planner`  *(v0.4)*
A* path planning over a coverage grid + greedy-nearest object pickup. Per CleanUpBench's reference baseline. Out of scope for v0.1 scaffold.

### 7.3 RL policies *(future)*
Out of scope until a separate Tier 2 charter introduces the training infrastructure.

## 8. Evaluation protocol

```
for split in [eval-known, eval-novel]:
    for vehicle in [sedan, suv, hatchback]:
        for task in [sweep_floor, pickup_objects, spot_clean_seat, full_clean]:
            for episode in 1..20:
                seed = (split_id, vehicle_id, task_id, episode_id)  # deterministic
                env = VICEnv(vehicle, task, seed=seed)
                rollout(env, policy)
                record per-episode metrics
        report mean ± std per metric per (vehicle, task)
```

A submission is an aggregated table of (split, vehicle, task) → (TCR, SE, MQ, CP, DA, VIC).

## 9. Reproducibility requirements

- Seeds: deterministic per `(split_id, vehicle_id, task_id, episode_id)` tuple.
- Sim version pinned in `pyproject.toml` (Isaac Sim 4.x once host machine is provisioned).
- Eval script logs per-step actions and observations to a parquet trace file.
- Hardware spec (GPU model, driver version) reported alongside results.

## 10. What this v0.1 spec does not commit to

- The exact procedural-generation parameters per vehicle class (will tune once Isaac host is online).
- The leaderboard / submission format (separate v1.0 release ADR).
- A "real" sim-to-real pipeline (out of scope until phys-sim transfer is justified).
- An adversarial / unsafe-action evaluation (separate `/cso` charter).
