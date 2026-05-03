def retriever_agent(state):
    # mock vector search
    return {
        **state,
        "similar_incidents": [{"fix": "restart service"}]
    }