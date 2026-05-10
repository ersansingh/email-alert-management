import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

llm_base_url = os.getenv("LLM_BASE_URL")
if llm_base_url:
    if not llm_base_url.endswith("/v1"):
        llm_base_url = llm_base_url + "/v1"
    llm = ChatOpenAI(model="gpt-4", openai_api_base=llm_base_url, openai_api_key="mock")
else:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY", "mock_key"))

def classifier_agent(state):
    prompt = f'''
    Analyze alert:
    {state.message}

    Return JSON:
    alert_type, service, root_cause, recommendation
    '''
    res = llm.invoke(prompt)

    return {"alert_type": res.content}