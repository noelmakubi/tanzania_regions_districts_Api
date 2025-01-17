from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Region, District

# Unda jedwali kwenye database
# Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def get_regions_and_districts(db: Session = Depends(get_db)):
    # Fetch all regions and their districts
    regions = db.query(Region).all()
    result = [
        {
            "name": region.name,
            "districts": [{"name": district.name} for district in region.districts]
        }
        for region in regions
    ]
    return {"data": result}


# Fetch mikoa yote
@app.get("/regions/")
def get_regions(db: Session = Depends(get_db)):
    regions = db.query(Region).all()
    return {"data": regions}

# Fetch wilaya Zote
@app.get("/districts/")
def get_districts(db: Session = Depends(get_db)):
    districts = db.query(District).all()
    return {"data": districts}

# Fetch wilaya zote za mkoa
@app.get("/regions/{region_id}/districts/")
def get_districts(region_id: int, db: Session = Depends(get_db)):
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    # return region.districts
    return {"data":{region.name:[region.districts]}}


# Kazi ya kuongeza mikoa na wilaya
@app.post("/regions/")
def create_region(name: str, db: Session = Depends(get_db)):
    region = Region(name=name)
    db.add(region)
    db.commit()
    db.refresh(region)
    return region


@app.post("/districts/")
def create_district(name: str, region_id: int, db: Session = Depends(get_db)):
    # Hakikisha region ipo
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    district = District(name=name, region_id=region_id)
    db.add(district)
    db.commit()
    db.refresh(district)
    return district