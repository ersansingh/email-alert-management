import os
from langchain.chat_models import ChatOpenAI

llm_base_url = os.getenv("LLM_BASE_URL")
llm = ChatOpenAI(model="gpt-4", openai_api_base=llm_base_url) if llm_base_url else ChatOpenAI(model="gpt-4")

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