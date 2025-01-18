from sqlalchemy.orm import Session
from models import RecipeCost
from schemas import RecipeCostCreate

def create_recipe_cost(db: Session, recipe: RecipeCostCreate):
    db_recipe = RecipeCost(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipe_cost(db: Session, recipe_id: int):
    return db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()

def update_recipe_cost(db: Session, recipe_id: int, recipe: RecipeCostCreate):
    db_recipe = db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()
    if db_recipe:
        for key, value in recipe.dict().items():
            setattr(db_recipe, key, value)
        db.commit()
        db.refresh(db_recipe)
    return db_recipe

def delete_recipe_cost(db: Session, recipe_id: int):
    recipe = db.query(RecipeCost).filter(RecipeCost.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe