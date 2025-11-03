from dataclasses import dataclass, field
from typing import Dict


@dataclass
class State:
    question: str = ""
    isEUA: bool = False
    query: str = ""
    result: str = ""
    manager_decision: Dict = field(default_factory=dict)
    insight_writer_response: str = ""
    insight_drawer_response: str = ""
    insight_reasoner_response: str = ""
    web_researcher_response: str = ""
    insight_editor_response: Dict = field(default_factory=dict)
