"""Contract Net Protocol (CNP) Multi-Agent Auction Engine
100% Python Standard Library.
"""

class ContractNetProtocol:
    """FIPA CNP manager and bidder auction coordinator."""
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent_id, cost_per_unit):
        self.agents[agent_id] = cost_per_unit

    def announce_and_award(self, task_name, required_effort):
        bids = []
        for a_id, cost_factor in self.agents.items():
            total_cost = required_effort * cost_factor
            bids.append((total_cost, a_id))

        if not bids:
            return None

        bids.sort()
        best_cost, winner = bids[0]
        return {
            "task": task_name,
            "awarded_to": winner,
            "cost": best_cost,
            "all_bids": [{"agent": a, "bid": c} for c, a in bids]
        }
