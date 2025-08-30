from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import vrp_cli
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType
from pathlib import Path


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        schemas: dict[str, str] = vrp_cli.get_json_schemas()
        for name, json_schema in schemas.items():
            generate(
                json_schema,
                input_file_type=InputFileType.JsonSchema,
                input_filename=f"{name}.json",
                output=Path(f"src/vrp_types/schemas/model_{name}.py"),
                output_model_type=DataModelType.PydanticV2BaseModel,
                field_constraints=True,
                use_annotated=True,
            )
