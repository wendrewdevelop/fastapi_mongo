from fastapi import FastAPI
from bootstrap import mongodb


app = FastAPI()
mongodb.install(app)