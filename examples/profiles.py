from vrp_types import cfg, mat, prg, solve
from pprint import pprint
import matplotlib.pyplot as plt
import random

n = 16

problem = prg.Problem(
    plan=prg.Plan(
        jobs=[
            prg.Job(
                id=f"job_{i}",
                deliveries=[
                    prg.JobTask(
                        demand=[1],
                        places=[
                            prg.JobPlace(duration=0.0, location=prg.Location(index=i))
                        ],
                    )
                ],
            )
            for i in range(1, n**2)
        ]
    ),
    fleet=prg.Fleet(
        profiles=[
            prg.MatrixProfile(name="normal"),
            prg.MatrixProfile(name="not-normal"),
        ],
        vehicles=[
            prg.VehicleType(
                typeId="vehicle_type_1",
                vehicleIds=[f"vehicle_1_{i}" for i in range(1, 30)],
                capacity=[12],
                costs=prg.VehicleCosts(distance=2.0, time=0.0, fixed=2000.0),
                profile=prg.VehicleProfile(matrix="normal"),
                shifts=[
                    prg.VehicleShift(
                        start=prg.ShiftStart(
                            earliest="2020-05-01T09:00:00.00Z",
                            location=prg.Location(index=0),
                        ),
                        end=prg.ShiftEnd(
                            latest="2020-05-01T18:00:00.00Z",
                            location=prg.Location(index=0),
                        ),
                    )
                ],
            ),
            prg.VehicleType(
                typeId="vehicle_type_2",
                vehicleIds=[f"vehicle_2_{i}" for i in range(1, 10)],
                capacity=[60],
                costs=prg.VehicleCosts(distance=1.0, time=0.0),
                profile=prg.VehicleProfile(matrix="not-normal"),
                shifts=[
                    prg.VehicleShift(
                        start=prg.ShiftStart(
                            earliest="2020-05-01T09:00:00.00Z",
                            location=prg.Location(index=0),
                        ),
                        end=prg.ShiftEnd(
                            latest="2020-05-01T18:00:00.00Z",
                            location=prg.Location(index=0),
                        ),
                    )
                ],
            ),
        ],
    ),
    objectives=[
        prg.Objective(type="minimize-unassigned"),
        prg.Objective(type="minimize-cost"),
    ],
)

random.seed(42)
coord_list = [
    (x * 1000 + random.randint(-100, 100), y * 1000 + random.randint(-100, 100))
    for y in range(n)
    for x in range(n)
][: n**2]
matrix = [
    mat.Matrix(
        distances=[
            round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
            for x1, y1 in coord_list
            for x2, y2 in coord_list
        ],
        travelTimes=[0] * (len(coord_list) ** 2),
        profile="normal",
    ),
    mat.Matrix(
        distances=[
            round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
            if ((max(x1, x2) < 3500) or (min(x1, x2) > 11500) or max(y1, y2) < 3500)
            else 10**9
            for x1, y1 in coord_list
            for x2, y2 in coord_list
        ],
        travelTimes=[0] * (len(coord_list) ** 2),
        profile="not-normal",
    ),
]

config = cfg.Config(
    termination=cfg.TerminationConfig(maxTime=60),
    telemetry=cfg.TelemetryConfig(progress=cfg.ProgressConfig(enabled=True)),
)

solution = solve(problem=problem, matrix=matrix, config=config)

plt.figure()
for tour in solution.tours:
    plt.plot(
        [coord_list[stop.root.location.root.index][0] for stop in tour.stops],
        [coord_list[stop.root.location.root.index][1] for stop in tour.stops],
        c=("blue" if tour.typeId == "vehicle_type_1" else "orange"),
    )
plt.scatter(
    [x for x, y in coord_list if min(x, y) < 3500 or x > 11500],
    [y for x, y in coord_list if min(x, y) < 3500 or x > 11500],
)
plt.scatter(
    [x for x, y in coord_list if not (min(x, y) < 3500 or x > 11500)],
    [y for x, y in coord_list if not (min(x, y) < 3500 or x > 11500)],
    marker="x",
)
plt.show()
pprint(solution.model_dump_json())
