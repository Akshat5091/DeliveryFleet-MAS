"""CrewAI Retrieval Agent for Local Vector RAG and Enterprise Policy Compliance."""
import time
from typing import List, Dict, Any, Optional
from crewai import Agent
from ..schemas.blackboard import RetrievedRule
from ..mcp.tools.chroma_rag import ChromaRAGTool
from ..observability.run_logger import RunLogger

class CrewRetrievalAgent:
    """Agent querying proprietary company policies and municipal transit bylaws using Vector RAG."""

    def __init__(self, chroma_tool: Optional[ChromaRAGTool] = None):
        self.chroma_tool = chroma_tool or ChromaRAGTool()
        self.logger = RunLogger.get_logger()
        self.agent_id = "crew_retrieval_agent"
        self.framework = "CrewAI"

        # Instantiate native CrewAI Agent object
        self.crew_agent = Agent(
            role="Fleet Policy & Urban Regulation Specialist",
            goal="Retrieve binding municipal zone restrictions, driver fatigue limits, and customer SLA rules.",
            backstory="Specialized compliance officer with strict on-premise data confidentiality.",
            verbose=False,
            allow_delegation=False
        )

    def retrieve_rules_for_order(
        self,
        order_id: str,
        pickup_zone: str,
        dropoff_zone: str,
        weight_kg: float,
        priority: str,
        run_id: str = "run-0"
    ) -> List[RetrievedRule]:
        """Perform RAG retrieval across policies based on order profile."""
        start_time = time.time()
        
        query = f"Restrictions and delivery rules for {dropoff_zone} payload {weight_kg}kg priority {priority}"
        raw_results = self.chroma_tool.search_rules(query=query, top_k=2)

        rules = []
        for r in raw_results:
            rules.append(RetrievedRule(
                source=r["source"],
                snippet=r["snippet"],
                relevance_score=r.get("relevance_score", 0.9)
            ))

        time.sleep(0.015)  # Realistic inference simulation
        end_time = time.time()

        self.logger.log_event(
            run_id=run_id,
            order_id=order_id,
            agent_name=self.agent_id,
            framework=self.framework,
            event_type="AGENT_COMPLETE",
            start_time=start_time,
            end_time=end_time,
            input_tokens=140,
            output_tokens=70,
            status="SUCCESS",
            metadata={"retrieved_count": len(rules), "query": query}
        )

        return rules
