from vrp_types import prg, mat, cfg, solve
import matplotlib.pyplot as plt

# fmt: off
coord_list = [
    (40, 40), (22, 22), (36, 26), (21, 45), (45, 35), (55, 20), (33, 34),
    (50, 50), (55, 45), (26, 59), (40, 66), (55, 65), (35, 51), (62, 35),
    (62, 57), (62, 24), (21, 36), (33, 44), (9, 56), (62, 48), (66, 14),
    (44, 13), (26, 13), (11, 28), (7, 43), (17, 64), (41, 46), (55, 34),
    (35, 16), (52, 26), (43, 26), (31, 76), (22, 53), (26, 29), (50, 40),
    (55, 50), (54, 10), (60, 15), (47, 66), (30, 60), (30, 50), (12, 17),
    (15, 14), (16, 19), (21, 48), (50, 30), (51, 42), (50, 15), (48, 21),
    (12, 38), (15, 56), (29, 39), (54, 38), (55, 57), (67, 41), (10, 70),
    (6, 25), (65, 27), (40, 60), (70, 64), (64, 4), (36, 6), (30, 20),
    (20, 30), (15, 5), (50, 70), (57, 72), (45, 42), (38, 33), (50, 4),
    (66, 8), (59, 5), (35, 60), (27, 24), (40, 20), (40, 37)
]
# fmt: on

problem = prg.Problem(
    fleet=prg.Fleet(
        profiles=[prg.MatrixProfile(name="normal")],
        vehicles=[
            prg.VehicleType(
                capacity=[1000],
                costs=prg.VehicleCosts(distance=1.0, time=0.0),
                profile=prg.VehicleProfile(matrix="normal"),
                shifts=[
                    prg.VehicleShift(
                        start=prg.ShiftStart(
                            earliest="2019-07-04T09:00:00Z",
                            location=prg.Location(index=0),
                        ),
                        end=prg.ShiftEnd(
                            latest="2019-07-04T17:00:00Z",
                            location=prg.Location(index=0),
                        ),
                    )
                ],
                vehicleIds=["vehicle_1"],
                typeId="normal",
            )
        ],
    ),
    plan=prg.Plan(
        jobs=[
            prg.Job(
                deliveries=[
                    prg.JobTask(
                        demand=[1],
                        places=[
                            prg.JobPlace(
                                duration=0.0,
                                location=prg.Location(index=index),
                            )
                        ],
                    )
                ],
                id=f"job_{index}",
            )
            for index in range(1, len(coord_list))
        ]
    ),
)

matrix = mat.Matrix(
    distances=[
        round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * 1000)
        for x1, y1 in coord_list
        for x2, y2 in coord_list
    ],
    travelTimes=[0] * (len(coord_list) ** 2),
    profile="normal",
)

config = cfg.Config(
    termination=cfg.TerminationConfig(maxTime=50),
    telemetry=cfg.TelemetryConfig(progress=cfg.ProgressConfig(enabled=True)),
)

solution = solve(problem=problem, matrix=[matrix], config=config)

for tour in solution.tours:
    plt.plot(
        [coord_list[stop.root.location.root.index][0] for stop in tour.stops],
        [coord_list[stop.root.location.root.index][1] for stop in tour.stops],
        marker="o",
    )
plt.show()

print(solution.model_dump_json())
