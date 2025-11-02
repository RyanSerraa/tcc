from dataclasses import dataclass, field
from typing import Dict


@dataclass
class State:
    question: str = ""
    isEUA: bool = False
    query: str = ""
    result: str = ""
    manager_decision: Dict = field(default_factory=dict)
    textEditor_response: str = ""
    chartEditor_response: str = ""
    analista_response: str = ""
    web_researcher_response: str = ""
    redator_response: Dict = field(default_factory=dict)
