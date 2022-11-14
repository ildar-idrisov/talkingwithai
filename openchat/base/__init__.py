from openchat.base.agents.base import BaseAgent, DecoderLM, EncoderLM, Seq2SeqLM, SingleTurn
from openchat.base.agents.parlai import ParlaiAgent, ParlaiClassificationAgent, ParlaiGenerationAgent
from openchat.base.agents.convai2 import ConvAI2Agent
from openchat.base.agents.huggingface import HuggingfaceAgent
from openchat.base.agents.prompt import PromptAgent
from openchat.base.agents.wow import WizardOfWikipediaAgent

__all__ = [
    BaseAgent,
    HuggingfaceAgent,
    ParlaiAgent,
    ParlaiGenerationAgent,
    ParlaiClassificationAgent,
    ConvAI2Agent,
    WizardOfWikipediaAgent,
    PromptAgent,
    EncoderLM,
    DecoderLM,
    Seq2SeqLM,
    SingleTurn,
]
