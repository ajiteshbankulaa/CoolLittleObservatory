from fastapi import Request

from app.services.registry import ServiceContainer


def get_container(request: Request) -> ServiceContainer:
    return request.app.state.container

