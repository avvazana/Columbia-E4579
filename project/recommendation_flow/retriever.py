from project.recommendation_flow.controllers.RandomController import RandomController
from project.data_models.content import Content, get_url
from project.data_models.user import User
from enum import Enum


class ControllerEnum(Enum):
    RANDOM = RandomController


def content_to_response(content):
    generated_content_metadata = content.generated_content_metadata[0]
    return {
        'id': content.id,
        'download_url': get_url(content),
        'author': generated_content_metadata.source,  # TODO: change to a query
        'text': f"""{generated_content_metadata.original_prompt}\n In the style of {generated_content_metadata.artist_style}"""
    }


def get_content_data(controller, user_id, limit, offset):
    if controller == ControllerEnum.RANDOM:
        content_ids = ControllerEnum.RANDOM.value().get_content_ids(user_id, limit, offset)
    else:
        raise ValueError(f"don't support that controller: {controller}")
    all_content = Content.query.filter(Content.id.in_(content_ids)).all()
    responses = map(content_to_response, all_content)
    return list(responses)
