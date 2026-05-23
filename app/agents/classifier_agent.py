import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

def classifier_agent(state):
    prompt = f'''
    Analyze alert:
    {state.message}

    Return JSON:
    alert_type, service, root_cause, recommendation
    '''
    res = llm.invoke(prompt)

    return {"alert_type": res.content}