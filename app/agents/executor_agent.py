import subprocess

def executor_agent(state):
    results = []

    for step in state.get("remediation_plan", []):
        try:
            cmd = step["action"]
            out = subprocess.run(cmd, shell=True, capture_output=True)

            results.append({
                "step": step["step"],
                "status": out.returncode
            })
        except Exception as e:
            results.append({"error": str(e)})

    return {**state, "execution_status": results}