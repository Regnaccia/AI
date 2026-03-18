from models.Project import ProjectStatus
from models.Project import BaseProject

from core.messager import compose_outbound_message
from core.messager import input_request


def route(pj):
    if pj.status == ProjectStatus.WAITING_PROMPT:
        message = compose_outbound_message(
            pj= pj,
            sender= "system",
            to= "user",
            content= "Hy how can i help you today?"
        )

        print(message.content) 
        inbound = input()
        message = input_request(
            pj= pj,
            sender= "user",
            to= pj.active_agent,
            content= inbound
        )
        pj.change_status(ProjectStatus.PROCESSING)