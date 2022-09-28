import time
from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, status, HTTPException, Cookie, Header, BackgroundTasks
from pydantic import BaseModel, Field


class Department(str, Enum):
    MATH = "math"
    ENGLISH = "english"
    CHEMISTRY = "chemistry"


class Employee(BaseModel):
    id: int = Field(description="The ID that the employee uses to login everywhere")
    department: Department = Field(description="The primary department of the employee")
    age: int = Field(description="The official age of the employee")
    gender: str = Field(
        default=None,
        description="The gender of the employee, if they want to disclose it",
        max_length=8
    )


class NotificationPayload(BaseModel):
    email: str
    notification_type: int


app = FastAPI(debug=True)


@app.get("/status")
async def check_status():
    return {"status": "ok"}


@app.get("/employees/{id}")
async def get_employees(id: int):
    print(id)
    return [
        {"id": 1, "name": "Bob"},
        {"id": 2, "name": "Mike"},
        {"id": 3, "name": "Jonh"},
    ]


@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: Employee):
    if employee.id in [200, 300, 400]:
        raise HTTPException(status_code=400, detail="Not a valid employee ID")
    print(employee)
    return employee


def send_notification(email: str):
    time.sleep(10)
    print(f'Done sending email to: {email}')


@app.post("/send-email")
async def send_email(
        background_tasks: BackgroundTasks,
        notification_payload: NotificationPayload,
        token: Optional[str] = Cookie(None),
        user_agent: Optional[str] = Header(None)
):
    print(notification_payload)

    background_tasks.add_task(send_notification, notification_payload.email)

    return {
        "cookie_received": token,
        "user_agent_received": user_agent,
        "custom_message": "I parsed everything",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
