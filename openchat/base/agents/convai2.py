from openchat.base import ParlaiGenerationAgent
from db.models import Prefix
from db.session import DB

class ConvAI2Agent(ParlaiGenerationAgent):

    def add_persona(self, histories, user_id, text):
        Prefix.add(user_id=user_id, prefix=f"your persona: {text}")
        histories[user_id]["prefix"].append(f"your persona: {text}")#TODO: delete histories

    def clear_persona(self, histories, user_id):
        session = DB.session()
        session.query(Prefix).filter(Prefix.user_id==user_id, Prefix.prefix.ilike('%your persona:%')).delete(synchronize_session=False)
        session.commit()
        histories[user_id]["prefix"] = [#TODO: delete histories
            pf for pf in histories[user_id]["prefix"]
            if "your persona:" not in pf
        ]
