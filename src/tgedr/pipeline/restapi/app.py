from fastapi import FastAPI

app = FastAPI(debug=True)

from tgedr.pipeline.restapi.scoring import api
