from pydantic import BaseModel


class RecipeModel(BaseModel):
    id: int
    title: str
    description: str
    ingredients: str
    steps: str
    time: int
    difficulty: int
    servings: int
