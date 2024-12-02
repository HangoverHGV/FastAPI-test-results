from pydantic import BaseModel


class RecipeModel(BaseModel):
    title: str
    description: str
    ingredients: str
    steps: str
    time: int
    difficulty: int
    servings: int
