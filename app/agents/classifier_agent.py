from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def classifier_agent(state):
    prompt = f'''
    Analyze alert:
    {state["message"]}

    Return JSON:
    alert_type, service, root_cause, recommendation
    '''
    res = llm.invoke(prompt)

    return {
        **state,
        "alert_type": res.content
    }