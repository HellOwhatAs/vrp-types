from vrp_types import cfg, mat, prg, solve
from itertools import chain
import matplotlib.pyplot as plt
import random
from math import ceil

n = 160
rows = 2

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
                skills=prg.JobSkills(allOf=[f"skill_{i % 2}"]),
            )
            for i in range(1, n)
        ]
    ),
    fleet=prg.Fleet(
        profiles=[prg.MatrixProfile(name="normal")],
        vehicles=[
            prg.VehicleType(
                typeId="vehicle_type_1",
                vehicleIds=[f"vehicle_1_{i}" for i in range(1, 10)],
                capacity=[12],
                costs=prg.VehicleCosts(distance=1.0, time=0.0),
                profile=prg.VehicleProfile(matrix="normal"),
                skills=["skill_0"],
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
                vehicleIds=[f"vehicle_2_{i}" for i in range(1, 2)],
                capacity=[100],
                costs=prg.VehicleCosts(distance=1.0, time=0.0),
                profile=prg.VehicleProfile(matrix="normal"),
                skills=["skill_0", "skill_1"],
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
)

random.seed(42)
coord_list = [
    (x * 1000 + random.randint(-100, 100), (y * 1000 + random.randint(-100, 100)) * 10)
    for y in range(rows)
    for x in range(ceil(n / rows))
][:n]
matrix = mat.Matrix(
    distances=list(
        chain.from_iterable(
            [round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) for x2, y2 in coord_list]
            for x1, y1 in coord_list
        )
    ),
    travelTimes=[0] * (len(coord_list) ** 2),
    profile="normal",
)

config = cfg.Config(
    termination=cfg.TerminationConfig(maxTime=50),
    telemetry=cfg.TelemetryConfig(progress=cfg.ProgressConfig(enabled=True)),
)

solution = solve(problem=problem, matrix=[matrix], config=config)

plt.figure()
for tour in solution.tours:
    plt.plot(
        [coord_list[stop.root.location.root.index][0] for stop in tour.stops],
        [coord_list[stop.root.location.root.index][1] for stop in tour.stops],
    )
plt.scatter([x for x, _ in coord_list[::2]], [y for _, y in coord_list[::2]])
plt.scatter(
    [x for x, _ in coord_list[1::2]], [y for _, y in coord_list[1::2]], marker="x"
)
plt.show()
print(solution.model_dump_json())
