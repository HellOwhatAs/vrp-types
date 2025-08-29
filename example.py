from vrp_types import prg, mat, cfg, solve

# fmt: off
matrix = mat.Matrix(
    profile="normal_car",
    travelTimes=[
        0, 609, 981, 906,
        813, 0, 371, 590,
        1055, 514, 0, 439,
        948, 511, 463, 0
    ],
    distances=[
        0, 3840, 5994, 5333,
        4696, 0, 2154, 3226,
        5763, 2674, 0, 2145,
        5112, 2470, 2152, 0,
    ],
)
# fmt: on


# specify termination criteria: max running time in seconds or max amount of refinement generations
config = cfg.Config(
    termination=cfg.TerminationConfig(
        maxTime=5,
        maxGenerations=1000,
    ),
    telemetry=cfg.TelemetryConfig(progress=cfg.ProgressConfig(enabled=True)),
)

# specify test problem
problem = prg.Problem(
    plan=prg.Plan(
        jobs=[
            prg.Job(
                id="delivery_job1",
                deliveries=[
                    prg.JobTask(
                        places=[
                            prg.JobPlace(
                                location=prg.Location(lat=52.52599, lng=13.45413),
                                duration=300,
                                times=[
                                    ["2019-07-04T09:00:00Z", "2019-07-04T18:00:00Z"]
                                ],
                            ),
                        ],
                        demand=[1],
                    )
                ],
            ),
            prg.Job(
                id="pickup_job2",
                pickups=[
                    prg.JobTask(
                        places=[
                            prg.JobPlace(
                                location=prg.Location(lat=52.5225, lng=13.4095),
                                duration=240,
                                times=[
                                    ["2019-07-04T10:00:00Z", "2019-07-04T16:00:00Z"]
                                ],
                            )
                        ],
                        demand=[1],
                    )
                ],
            ),
            prg.Job(
                id="pickup_delivery_job3",
                pickups=[
                    prg.JobTask(
                        places=[
                            prg.JobPlace(
                                location=prg.Location(lat=52.5225, lng=13.4095),
                                duration=300,
                                tag="p1",
                            )
                        ],
                        demand=[1],
                    )
                ],
                deliveries=[
                    prg.JobTask(
                        places=[
                            prg.JobPlace(
                                location=prg.Location(lat=52.5165, lng=13.3808),
                                duration=300,
                                tag="d1",
                            ),
                        ],
                        demand=[1],
                    )
                ],
            ),
        ]
    ),
    fleet=prg.Fleet(
        vehicles=[
            prg.VehicleType(
                typeId="vehicle",
                vehicleIds=["vehicle_1"],
                profile=prg.VehicleProfile(matrix="normal_car"),
                costs=prg.VehicleCosts(fixed=22, distance=0.0002, time=0.005),
                shifts=[
                    prg.VehicleShift(
                        start=prg.ShiftStart(
                            earliest="2019-07-04T09:00:00Z",
                            location=prg.Location(lat=52.5316, lng=13.3884),
                        ),
                        end=prg.ShiftEnd(
                            latest="2019-07-04T18:00:00Z",
                            location=prg.Location(lat=52.5316, lng=13.3884),
                        ),
                    )
                ],
                capacity=[10],
            )
        ],
        profiles=[prg.MatrixProfile(name="normal_car")],
    ),
)

solution = solve(problem=problem, matrix=[matrix], config=config)
print(solution.model_dump_json(indent=4))
