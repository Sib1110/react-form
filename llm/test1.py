import re
import subprocess
from smolagents import CodeAgent, OpenAIServerModel, tool

MAIN   = "https://wins9ctf.aws-king.co.kr/"
TARGET = "http://wins9ctf.aws-king.co.kr:32773"
FLAG_RE = r"(?:FLAG|flag)\{[^}]{1,100}\}"

model = OpenAIServerModel(
    model_id="ctf",
    api_base="http://localhost:8000/v1",
    api_key="dummy",
    temperature=0.2,
    max_tokens=1024,
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
    return out[:1200] + ("\n...[truncated]" if len(out) > 1200 else "")


def new_agent(max_steps=8):
    return CodeAgent(
        tools=[run_bash],
        model=model,
        additional_authorized_imports=["requests", "re", "base64", "json",
                                       "urllib.parse", "hashlib", "socket"],
        max_steps=max_steps,
    )


def find_flag(text):
    m = re.search(FLAG_RE, str(text))
    return m.group(0) if m else None


# ---------- 1단계: 정찰 ----------
recon = new_agent(max_steps=8).run(f"""
대상 사이트를 정찰하라.
- 메인: {MAIN}
- 문제 인스턴스: {TARGET}

점검: robots.txt, 응답 헤더, HTML 주석, 쿠키, 링크, 폼, /admin 같은 흔한 경로.
규칙: 응답은 반드시 앞 1000자만 print. 큰 출력은 | head -30 사용.

끝나면 '발견한 단서'를 5줄 이내로 요약하되,
다음 단계가 바로 쓸 수 있게 구체적 URL, 파라미터 이름, 발견값을 포함해
final_answer 로 제출하라.
""")
print("\n===== 정찰 요약 =====\n", recon)

flag = find_flag(recon)
if flag:
    print("\n[+] 정찰 단계에서 플래그 발견:", flag)
    raise SystemExit

# ---------- 2단계: 공략 ----------
result = new_agent(max_steps=10).run(f"""
대상: {TARGET}

이전 정찰 요약:
{recon}

위 단서를 바탕으로 취약점을 공략해 플래그를 찾아라.
후보 취약점: SQLi, LFI, 명령주입, 인증우회, 숨은 파라미터, 쿠키 조작 등.
규칙: 응답은 앞 1000자만 print. 플래그 형식은 FLAG{{...}} 또는 flag{{...}}.
플래그를 찾으면 final_answer(플래그) 로 제출하라.
""")
print("\n===== 공략 결과 =====\n", result)

flag = find_flag(result)
print("\n[+] 최종 플래그:", flag if flag else "미발견 — 요약을 보고 2단계를 재시도하세요.")
