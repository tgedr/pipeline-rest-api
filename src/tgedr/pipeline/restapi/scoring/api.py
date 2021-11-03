import datetime
import logging
import uuid
from uuid import UUID
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response
from tgedr.pipeline.restapi.app import app
from tgedr.pipeline.restapi.scoring.schemas import ScoringModelSchema, NewScoringModelSchema, ScoringModelsSchema

logger = logging.getLogger(__name__)

models = []


@app.get('/scoring/', response_model=ScoringModelsSchema)
def get_scoring_models():
    logger.info("[get_scoring_models|in]")
    global models
    logger.info(f"[get_scoring_models|out] => {models}")
    return {'models': models}


@app.post('/scoring', status_code=status.HTTP_201_CREATED, response_model=ScoringModelSchema)  # noqa: E501
def create_scoring_model(scoring_model: NewScoringModelSchema):
    logger.info(f"[create_scoring_model|in] ({scoring_model})")
    model = scoring_model.dict()
    model['id'] = uuid.uuid4()
    model['created'] = datetime.datetime.utcnow()
    global models
    models.append(model)
    logger.info(f"[create_scoring_model|out] => {model}")
    return model


@app.get('/scoring/{model_id}', response_model=ScoringModelSchema)
def get_scoring_model(model_id: UUID):
    for model in models:
        if model['id'] == model_id:
            return model
    raise HTTPException(
        status_code=404, detail=f'model with ID {model_id} not found'
    )


@app.put('/scoring/{model_id}', response_model=ScoringModelSchema)
def update_scoring_model(model_id: UUID, scoring_model: ScoringModelSchema):
    for model in models:
        if model['id'] == model_id:
            model.update(scoring_model)
            return model
    raise HTTPException(
        status_code=404, detail=f'model with ID {model_id} not found'
    )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_scoring_model(model_id: UUID):
    for index, model in enumerate(models):
        if model['id'] == model_id:
            models.pop(index)
            return
    raise HTTPException(
        status_code=404, detail=f'model with ID {model_id} not found'
    )