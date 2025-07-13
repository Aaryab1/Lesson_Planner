import requests

response = requests.post(
    "http://localhost:8000/create-lesson-plan",
    json={"topic": "Photosynthesis", "grade_level": "grade 5"}
)
print(response.json())