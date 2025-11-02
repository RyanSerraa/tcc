from dataclasses import dataclass, field
from typing import Dict


@dataclass
class State:
    question: str = ""
    isEUA: bool = False
    query: str = ""
    result: str = ""
    manager_decision: Dict = field(default_factory=dict)
    insight_writer_agent: str = ""
    insight_drawer_agent: str = ""
    insight_reasoner_agent: str = ""
    web_researcher_agent: str = ""
    insight_editor_agent: Dict = field(default_factory=dict)
