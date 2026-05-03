from app.agents.graph import graph

def process_alert(payload):
    return graph.invoke(payload)