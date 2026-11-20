import subprocess
from smolagents import CodeAgent, OpenAIServerModel, tool

model = OpenAIServerModel(
    model_id="ctf",                          # --served-model-name 값
    api_base="http://localhost:8000/v1",     # vLLM 서버가 같은 머신이면 localhost
    api_key="dummy",
    temperature=0.2,
    max_tokens=2048,
)

@tool
def run_bash(cmd: str) -> str:
    """Run a bash command in the CTF VM and return its output (truncated).

    Args:
        cmd: The bash command to execute.
    """
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=60)
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "[timeout after 60s]"
    return out[:3000] + ("\n...[truncated]" if len(out) > 3000 else "")

agent = CodeAgent(
    tools=[run_bash],
    model=model,
    additional_authorized_imports=["requests", "re", "base64", "json",
                                   "urllib.parse", "hashlib", "bs4", "socket"],
    max_steps=40,
)

task = """
CTF 웹 문제를 풀어서 플래그를 찾아라.

대상:
- 메인 사이트: https://wins9ctf.aws-king.co.kr/
- 문제 인스턴스: http://wins9ctf.aws-king.co.kr:32772

목표: 플래그(형식을 모르면 FLAG{...} 또는 flag{...} 로 가정)를 찾는다.

지침:
- requests 또는 run_bash(curl 등)로 대상을 탐색한다.
- 응답은 필요한 부분만 print 한다. HTML 전체를 출력하지 말 것 (앞 1500자 정도만).
- robots.txt, 소스 주석, 쿠키, 숨은 파라미터, 흔한 웹 취약점(SQLi, LFI, 명령주입, 인증우회 등)을 점검한다.
- 플래그를 찾으면 즉시 final_answer(플래그)로 제출한다.
"""

print(agent.run(task))
