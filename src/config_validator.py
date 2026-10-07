import re
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import ClassVar, Any


class Level(BaseModel):
    """Store the settings for one game level"""
    level_num: int = 1
    width: int = 15
    height: int = 15
    default_levels: ClassVar[list[dict[str, int]]] = [
        {"level_num": 1, "height": 15, "width": 15},
        {"level_num": 2, "height": 15, "width": 17},
        {"level_num": 3, "height": 15, "width": 19},
        {"level_num": 4, "height": 15, "width": 20},
        {"level_num": 5, "height": 18, "width": 18},
        {"level_num": 6, "height": 18, "width": 20},
        {"level_num": 7, "height": 19, "width": 18},
        {"level_num": 8, "height": 15, "width": 20},
        {"level_num": 9, "height": 17, "width": 17},
        {"level_num": 10, "height": 17, "width": 20},
                                                    ]

    @field_validator("level_num")
    @classmethod
    def validate_level_num(cls, value: int | None) -> int | None:
        """Check that the level number is between 1 and 10"""
        if value is None or value < 1 or value > 10:
            print("Warning: level number should be from 1-10")
            return None
        return value

    @field_validator("width")
    @classmethod
    def validate_width(cls, value: int | None) -> int | None:
        """Check that the level width is between 15 and 60"""
        if value is None or value < 15 or value > 60:
            print("Width Out of range")
            return None
        return value

    @field_validator("height")
    @classmethod
    def validate_height(cls, value: int | None) -> int | None:
        """Check that the level height is between 15 and 60"""
        if value is None or value < 15 or value > 60:
            print("Height Out of range")
            return None
        return value


class Config(BaseModel):
    """Store and validate the game config"""
    highscore_filename: str = "highscore.json"
    level: list[Level] = Field(default_factory=list)
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42

    @field_validator("seed")
    @classmethod
    def validate_seed(cls, value: int | None) -> int | None:
        """Check that the seed is not negative"""
        if value is not None and value < 0:
            print("Warnning: the seed should be positive")
            return 42
        return value

    @field_validator("points_per_pacgum")
    @classmethod
    def validate_points_per_pacgum(cls, value: int | None) -> int:
        """Check that pacgum points are not negative"""
        if value is None or value <= 0:
            print("points_per_pacgum can't be negative or zero ")
            return 10
        return value

    @field_validator("points_per_super_pacgum")
    @classmethod
    def validate_points_per_super_pacgum(cls, value: int | None) -> int:
        """Check that Super Pac-Gum points are not negative"""
        if value is None or value <= 0:
            print("points_per_super_pacgum can't be negative or zero ")
            return 50
        return value

    @field_validator("points_per_ghost")
    @classmethod
    def validate_points_per_ghost(cls, value: int | None) -> int:
        """Check that ghost points are not negative"""
        if value is None or value <= 0:
            print("points_per_ghost can't be negative or zero ")
            return 200
        return value

    @field_validator("lives")
    @classmethod
    def validate_lives(cls, value: int | None) -> int:
        """Check that the number of lives is between 1 and 4"""
        if value is None or value < 1 or value > 4:
            print("Warnning: lives should not be less than 1 and more than 4")
            return 3
        return value

    @model_validator(mode="after")
    def set_default_levels(self) -> "Config":
        """Fill missing levels with default levels"""
        levels = []
        for index in range(10):
            default = Level.default_levels[index]
            if index < len(self.level):
                level = self.level[index]
                if level.level_num is None:
                    level.level_num = default["level_num"]
                if level.height is None:
                    level.height = default["height"]
                if level.width is None:
                    level.width = default["width"]
                levels.append(level)
            else:
                levels.append(Level(**default))
        self.level = levels
        return self

    @model_validator(mode="before")
    @classmethod
    def Check_missing(cls, data: dict[str, Any]) -> dict[str, Any]:
        """warn about missing config values"""
        defaults = {
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "lives": 3,
            "seed": 42,
        }
        for key, default in defaults.items():
            if key not in data:
                print(f"{key} is missing, using default value {default}")
        if "level" in data:
            for index, level in enumerate(data["level"]):
                defaultl = Level.default_levels[index]

                if "level_num" not in level:
                    print(
                        f"level {index + 1} level_num is missing, "
                        f"using default value {defaultl['level_num']}"
                    )

                if "height" not in level:
                    print(
                        f"level {index + 1} height is missing, "
                        f"using default value {defaultl['height']}"
                    )

                if "width" not in level:
                    print(
                        f"level {index + 1} width is missing, "
                        f"using default value {defaultl['width']}"
                    )
        return data


def read_config(config_json: str) -> Config:
    """Read , clean, and validate the JSON config file"""
    with open(config_json, "r") as file:
        data = file.read()
    data = re.sub(r"^\s*(#|//).*?$", "", data, flags=re.MULTILINE)
    if not data.strip():
        print("Warning:config file is empty")
        return Config()
    config: Config = Config.model_validate_json(data)
    return config
