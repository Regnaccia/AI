from models.Project import ProjectStatus

from core.messager import compose_outbound_message

def route(pj):
    if pj.status == ProjectStatus.WAITING_PROMPT:
        message = compose_outbound_message(
            pj= pj,
            sender= "system",
            to= "user",
            message= "Hy how can i help you today?"
        )
        print("message")
        print(message) 