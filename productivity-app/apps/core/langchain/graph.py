from typing import List
from langgraph.graph import StateGraph, END
from core.langchain.state import LLMState
from core.langchain.nodes.nodes import LLMNodes


class LLMFLow:
    def __init__(self, llm):
        self.nodes = LLMNodes(llm)
        self.graph = None

    def _build_graph(self):
        builder = StateGraph(LLMState)

        builder.add_node('write_post', self.nodes.write_post)
        builder.add_node('write_comment', self.nodes.write_comment)

        builder.set_conditional_entry_point(self.nodes.decide_action,
                                            {'write_post': 'write_post',
                                            'write_comment': 'write_comment'})

        builder.add_edge('write_post', END)
        builder.add_edge('write_comment', END)

        self.graph = builder.compile()

        return self.graph

    def run(self, personality: str, action: str, previous_messages: List = []) -> dict:
        if not self.graph:
            self._build_graph()

        init_state = LLMState(personality=personality, action=action,
                              previous_messages=previous_messages)

        return self.graph.invoke(init_state)
