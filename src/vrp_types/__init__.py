import vrp_types.schemas.model_solution as sol
import vrp_types.schemas.model_config as cfg
import vrp_types.schemas.model_matrix as mat
import vrp_types.schemas.model_problem as prg
import vrp_cli


def solve(
    problem: prg.Problem, matrix: list[mat.Matrix], config: cfg.Config
) -> sol.Solution:
    return sol.Solution.model_validate_json(
        vrp_cli.solve_pragmatic(
            problem=problem.model_dump_json(),
            matrices=[i.model_dump_json() for i in matrix],
            config=config.model_dump_json(),
        )
    )
