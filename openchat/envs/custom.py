import gc
import random

import torch

from openchat.base import BaseAgent, ConvAI2Agent, PromptAgent, SingleTurn, WizardOfWikipediaAgent
from openchat.base.envs.base import BaseEnvironment


class CustomEnvironment(BaseEnvironment):

    def __init__(self):
        super().__init__()

    def start(self, agent: BaseAgent):
        gc.enable()
        torch.cuda.empty_cache()

    def setup_persona(self, agent: BaseAgent, user_id, init_message):
        self.clear_histories(user_id)
        self.pre_dialog_output = self.pre_dialog_for_special_tasks(agent, user_id, init_message)

    def message(self, agent, user_id, input_message):
        torch.cuda.empty_cache()

        if isinstance(agent, PromptAgent):
            user_name, bot_name = self.pre_dialog_output
            user_message = input_message  # user_name.upper()
        else:
            user_message = input_message

        if isinstance(agent, WizardOfWikipediaAgent):
            user_message = agent.retrieve_knowledge(user_message)

        if isinstance(agent, PromptAgent):
            user_message = f"{user_name}: {user_message} {bot_name}:"

        if isinstance(agent, SingleTurn):
            model_input = user_message
        else:
            model_input = self.make_model_input(
                user_id,
                user_message,
                agent,
            )

        self.add_user_message(user_id, user_message)

        if isinstance(agent, PromptAgent):
            bot_message = agent.predict(
                model_input,
                person_1=user_name,
                person_2=bot_name,
            )["output"]

        else:
            bot_message = agent.predict(model_input)["output"]

        self.add_bot_message(user_id, bot_message)
        gc.collect()

        return bot_message

    def pre_dialog_for_special_tasks(self, agent, user_id, init_message):
        if isinstance(agent, ConvAI2Agent):
            return self.pre_dialog_for_convai2(agent, user_id, init_message)

        if isinstance(agent, WizardOfWikipediaAgent):
            return self.pre_dialog_for_wow(agent, user_id)

        if isinstance(agent, PromptAgent):
            return self.pre_dialog_for_prompt(agent, user_id)

    def pre_dialog_for_prompt(self, agent, user_id):
        user_name = cinput(
            "[YOUR NAME]: ",
            color=self.special_color,
        )

        bot_name = cinput(
            f"[{agent.name.upper()}'s NAME]: ",
            color=self.special_color,
        )

        agent.name = bot_name

        cprint(
            f"\n[SYSTEM]: Please input story you want.\n"
            f"[SYSTEM]: The story must contains '{user_name}' and '{bot_name}'.\n",
            color=self.system_color)

        story = cinput(
            "[STORY]: ",
            color=self.special_color,
        )

        while (user_name not in story) or (bot_name not in story):
            cprint(
                f"\n[SYSTEM]: Please input story you want.\n"
                f"[SYSTEM]: The story MUST contains '{user_name}' and '{bot_name}'.\n",
                color=self.system_color)

            story = cinput(
                "[STORY]: ",
                color=self.special_color,
            )

        cprint(
            "[STORY]: Story setting complete.\n",
            color=self.special_color,
        )

        story += f" {user_name} and {bot_name} start talking. "
        story += f"{user_name}: Hello {bot_name}. "
        story += f"{bot_name}: Hi {user_name}. "

        agent.add_prompt(
            self.histories,
            user_id,
            story,
        )

        return user_name, bot_name

    def pre_dialog_for_convai2(self, agent, init_message, user_id):
        agent.clear_persona(self.histories, user_id)
        agent.add_persona(self.histories, user_id, init_message)

    def pre_dialog_for_wow(self, agent, user_id):
        cprint(
            "[SYSTEM]: Please input topic for Wizard of wikipedia.\n"
            "[SYSTEM]: Enter '.topic' if you want to check random topic examples.\n",
            color=self.system_color)

        while True:
            _topic = cinput(
                "[TOPIC]: ",
                color=self.special_color,
            )

            if _topic == ".topic":
                random_list = agent.topic_list
                random.shuffle(random_list)
                random_list = random_list[:4]

                _topic = cprint(
                    f"[TOPIC]: {random_list}\n",
                    color=self.special_color,
                )

            else:
                if _topic in agent.topic_list:
                    cprint(
                        "[TOPIC]: Topic setting complete.\n",
                        color=self.special_color,
                    )
                    agent.set_topic(_topic)
                    break
                else:
                    _topic = cprint(
                        f"[TOPIC]: Wrong topic: {_topic}. Please enter validate topic.\n",
                        color=self.special_color,
                    )
