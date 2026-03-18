from models.messages import OutboundMessage

def compose_outbound_message(pj, sender, to, message):
    message = OutboundMessage(
        sender=sender,
        to=to, 
        message= message
        )
    pj.save_message_in_hystory(message.model_dump())
    return message