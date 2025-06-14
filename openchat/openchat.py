from openchat.agents.blender import BlenderGenerationAgent
from openchat.agents.dialogpt import DialoGPTAgent
from openchat.agents.dodecathlon import DodecathlonAgent
from openchat.agents.gptneo import GPTNeoAgent
from openchat.agents.reddit import RedditAgent
from openchat.agents.safety import OffensiveAgent, SensitiveAgent
from openchat.agents.unlikelihood import UnlikelihoodAgent
from openchat.agents.wow import WizardOfWikipediaGenerationAgent
from openchat.envs.custom import CustomEnvironment
from openchat.envs.interactive import InteractiveEnvironment
from openchat.utils.terminal_utils import draw_openchat


class OpenChat(object):

    def __init__(
        self,
        model,
        device,
        maxlen=-1,
        environment="interactive",
    ):
        draw_openchat()
        self.agent = self.check_agent(model)
        self.agent = self.create_agent_by_name(
            name=self.agent,
            device=device,
            maxlen=maxlen,
        )

        self.environment = self.check_environment(environment)
        self.environment = self.create_environment_by_name(environment)

    def start(self):
        self.environment.start(self.agent)

    def setup_persona(self, user_id, init_message):
        self.environment.setup_persona(self.agent, user_id, init_message)

    def predict_message(self, user_id, input_message):
        response_message = self.environment.message(self.agent, user_id, input_message)
        return response_message

    def check_agent(self, model) -> str:
        model = model.lower()
        available_models = self.available_models()

        assert model in available_models, \
            f"param `model` must be one of {available_models}"

        return model

    def check_environment(self, env):
        env = env.lower()
        available_envs = self.available_environments()

        assert env in available_envs, \
            f"param `environment` must be one of {available_envs}"

        return env

    def create_environment_by_name(self, name):
        if name == "interactive":
            return InteractiveEnvironment()
        elif name == "interactive_web":
            return InteractiveWebEnvironment()
        elif name == "webserver":
            raise NotImplementedError
        elif name == "facebook":
            raise NotImplementedError
        elif name == "kakaotalk":
            raise NotImplementedError
        elif name == "whatsapp":
            raise NotImplementedError
        elif name == "custom":
            return CustomEnvironment()

    def create_agent_by_name(self, name, device, maxlen):
        agent_name = name.split(".")[0]

        if agent_name == "blender":
            return BlenderGenerationAgent(name, device, maxlen)
        elif agent_name == "gptneo":
            return GPTNeoAgent(name, device, maxlen)
        elif agent_name == "dialogpt":
            return DialoGPTAgent(name, device, maxlen)
        elif agent_name == "dodecathlon":
            return DodecathlonAgent(name, device, maxlen)
        elif agent_name == "reddit":
            return RedditAgent(name, device, maxlen)
        elif agent_name == "unlikelihood":
            return UnlikelihoodAgent(name, device, maxlen)
        elif agent_name == "wizard_of_wikipedia":
            return WizardOfWikipediaGenerationAgent(name, device, maxlen)
        elif agent_name == "safety":
            if name.split(".")[1] == "offensive":
                return OffensiveAgent(name, device, maxlen)
            elif name.split(".")[1] == "sensitive":
                return SensitiveAgent(name, device, maxlen)
            else:
                return Exception("wrong model")
        else:
            return Exception("wrong model")

    @staticmethod
    def available_models():
        agents = [
            BlenderGenerationAgent,
            DialoGPTAgent,
            GPTNeoAgent,
            DodecathlonAgent,
            RedditAgent,
            SensitiveAgent,
            OffensiveAgent,
            UnlikelihoodAgent,
            WizardOfWikipediaGenerationAgent,
        ]

        available_models = []

        for agent in agents:
            available_models += agent.available_models()

        return available_models

    @staticmethod
    def available_environments():
        return [
            "interactive",
            "custom",
            # "webserver",
            # "facebook",
            # "kakaotalk",
            # "flask",
            # "whatsapp",
            # TODO: Future works
        ]
