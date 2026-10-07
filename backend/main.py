from unittest import result

from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from database import Base, engine, get_db
from models import Incident, User
from schemas import (
    IncidentAssign,
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
    UserCreate,
    UserResponse,
)


app = FastAPI(title="Enterprise Incident Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def get_admin_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user
def get_assigned_username(incident, db):
    if incident.assigned_to is None:
        return None

    user = db.query(User).filter(
        User.id == incident.assigned_to
    ).first()

    if user is None:
        return None

    return user.username

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Incident Management API is running"}


@app.get("/db-test")
def db_test():
    try:
        with engine.connect():
            return {"database": "Connected successfully"}
    except Exception as e:
        return {
            "database": "Connection failed",
            "error": str(e)
        }


@app.post("/incidents", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_incident = Incident(
        title=incident.title,
        description=incident.description,
        priority=incident.priority,
        status=incident.status,
        assigned_to=incident.assigned_to,
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    result = IncidentResponse.model_validate(new_incident)
    result.assigned_username = get_assigned_username(new_incident, db)

    return result


@app.get("/incidents", response_model=list[IncidentResponse])
def get_incidents(
    status: str | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Incident)

    if status:
        query = query.filter(Incident.status == status)

    if priority:
        query = query.filter(Incident.priority == priority)

    incidents = query.offset(skip).limit(limit).all()

    results = []

    for incident in incidents:
        result = IncidentResponse.model_validate(incident)
        result.assigned_username = get_assigned_username(incident, db)
        results.append(result)

    return results


@app.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    result = IncidentResponse.model_validate(incident)
    result.assigned_username = get_assigned_username(incident, db)

    return result


@app.put("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.title = incident_data.title
    incident.description = incident_data.description
    incident.priority = incident_data.priority
    incident.status = incident_data.status

    db.commit()
    db.refresh(incident)

    result = IncidentResponse.model_validate(incident)
    result.assigned_username = get_assigned_username(incident, db)

    return result


@app.put("/incidents/{incident_id}/assign", response_model=IncidentResponse)
def assign_incident(
    incident_id: int,
    assignment: IncidentAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    if assignment.assigned_to is not None:
       user = db.query(User).filter(
        User.id == assignment.assigned_to
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )

    incident.assigned_to = assignment.assigned_to

    db.commit()
    db.refresh(incident)

    result = IncidentResponse.model_validate(incident)
    result.assigned_username = get_assigned_username(incident, db)

    return result


@app.delete("/incidents/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return {"message": "Incident deleted successfully"}
@app.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    return db.query(User).all()

@app.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }