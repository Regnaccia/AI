from models.messages import OutboundMessage ,InboundMessage

def compose_outbound_message(pj, sender, to, content):
    message = OutboundMessage(
        sender=sender,
        to=to, 
        content= content,
        require_user_input= True
        )
    pj.save_message_in_hystory(message.model_dump())
    return message 

def input_request(pj, sender, to, content):
    message = InboundMessage(
        sender=sender,
        to=to, 
        content= content,
        )
    pj.save_message_in_hystory(message.model_dump())
    return message 