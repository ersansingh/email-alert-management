import os
from langchain_openai import ChatOpenAI

llm_base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
if not llm_base_url.endswith("/v1"):
    llm_base_url = llm_base_url + "/v1"

# Use openrouter/free as requested
llm = ChatOpenAI(
    model="openrouter/free", 
    openai_api_base=llm_base_url, 
    openai_api_key=os.getenv("OPENROUTER_API_KEY")
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
