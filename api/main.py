from fastapi import FastAPI, Depends
import models
from models import Recipe
from schema import RecipeModel
from database import SessionLocal, engine
from wait_for_db import wait_for_db
from tests.module import router

wait_for_db()

app = FastAPI()

app.include_router(router, prefix="/tests")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/recipe", tags=["recipe"])
def read_recipe(db: SessionLocal = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes

@app.get("/recipe/{recipe_id}", tags=["recipe"])
def read_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    return recipe

@app.post("/recipe", tags=["recipe"])
def create_recipe(recipe: RecipeModel, db: SessionLocal = Depends(get_db)):
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        time=recipe.time,
        difficulty=recipe.difficulty,
        servings=recipe.servings
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/recipe/{recipe_id}", tags=["recipe"])
def delete_recipe(recipe_id: int, db: SessionLocal = Depends(get_db)):
    db.query(Recipe).filter(Recipe.id == recipe_id).delete()
    db.commit()
    return {"message": "Recipe deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
