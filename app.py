from fastapi import FastAPI
from pydantic import BaseModel
from dataclasses import dataclass

app = FastAPI()

STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

def gregorian_to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return (
        d
        + (153 * m2 + 2) // 5
        + 365 * y2
        + y2 // 4
        - y2 // 100
        + y2 // 400
        - 32045
    )

def mod(n: int, m: int) -> int:
    return (n % m + m) % m

class DateInput(BaseModel):
    date: str  # "YYYY-MM-DD"

@app.post("/ilgan")
def get_ilgan(data: DateInput):
    y, m, d = map(int, data.date.split("-"))
    jdn = gregorian_to_jdn(y, m, d)

    stem_idx = 1 + mod(jdn - 1, 10)
    branch_idx = 1 + mod(jdn + 1, 12)

    ilgan = STEMS[stem_idx - 1]
    ilji = BRANCHES[branch_idx - 1]

    return {
        "ilgan": ilgan,
        "ilju": f"{ilgan}{ilji}"
    }