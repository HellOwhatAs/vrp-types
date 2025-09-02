from vrp_types import cfg, mat, prg, solve
import matplotlib.pyplot as plt
import random
from cycler import Cycler

n = 10

problem = prg.Problem(
    plan=prg.Plan(
        jobs=[
            prg.Job(
                id=f"job_{i}",
                pickups=[
                    prg.JobTask(
                        demand=[10],
                        places=[
                            prg.JobPlace(
                                duration=0.0, location=prg.Location(index=2 * i + 1)
                            )
                        ],
                    )
                ],
                deliveries=[
                    prg.JobTask(
                        demand=[10],
                        places=[
                            prg.JobPlace(
                                duration=0.0, location=prg.Location(index=2 * (i + 1))
                            )
                        ],
                    )
                ],
            )
            for i in range(n)
        ]
        + [
            prg.Job(
                id=f"job_pickups_{i}",
                pickups=[
                    prg.JobTask(
                        demand=[1],
                        places=[
                            prg.JobPlace(duration=0.0, location=prg.Location(index=i))
                        ],
                    )
                ],
            )
            for i in range(2 * n + 1, 4 * n + 1)
        ]
    ),
    fleet=prg.Fleet(
        profiles=[prg.MatrixProfile(name="normal")],
        vehicles=[
            prg.VehicleType(
                typeId="vehicle_type_1",
                vehicleIds=[f"vehicle_1_{i}" for i in range(1, 30)],
                capacity=[10],
                costs=prg.VehicleCosts(distance=1.0, time=0.0),
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
        ],
    ),
)

random.seed(42)
coord_list = (
    [(0, 0)]
    + [(x * 1000, y * 1000) for x in range(1, n + 1) for y in range(-1, 2, 2)]
    + [(x * 1000, y * 1000) for x in range(1, n + 1) for y in range(2, 4)]
)
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
]

config = cfg.Config(
    termination=cfg.TerminationConfig(maxTime=40),
    telemetry=cfg.TelemetryConfig(progress=cfg.ProgressConfig(enabled=True)),
)

solution = solve(problem=problem, matrix=matrix, config=config)

plt.figure()
color_cycler: Cycler = plt.rcParams["axes.prop_cycle"]
for tour, color in zip(solution.tours, color_cycler()):
    x = [coord_list[stop.root.location.root.index][0] for stop in tour.stops]
    y = [coord_list[stop.root.location.root.index][1] for stop in tour.stops]
    for i in range(len(x) - 1):
        plt.annotate(
            "",
            xy=(x[i + 1], y[i + 1]),
            xytext=(x[i], y[i]),
            arrowprops=dict(arrowstyle="->", color=color["color"], lw=2),
        )

plt.scatter(
    [x for x, _ in coord_list[1 : 2 * n + 1 : 2]],
    [y for _, y in coord_list[1 : 2 * n + 1 : 2]],
    marker="s",
    c="blue",
)
plt.scatter(
    [x for x, _ in coord_list[2 : 2 * n + 1 : 2]],
    [y for _, y in coord_list[2 : 2 * n + 1 : 2]],
    c="blue",
)
plt.scatter(
    [x for x, _ in coord_list[2 * n + 1 :]],
    [y for _, y in coord_list[2 * n + 1 :]],
    marker="s",
    c="green",
)
plt.scatter(
    [x for x, _ in coord_list[:1]],
    [y for _, y in coord_list[:1]],
    marker="*",
    s=100,
    c="red",
)

plt.axis("equal")
plt.show()
print(solution.model_dump_json())
