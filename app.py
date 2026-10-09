"""AI 销售顾问 · Web 演示页（Streamlit）

一键部署用。有模型 key 就真调用，没 key 就展示拼好的完整提示词，
让用户复制去 Grok Bot 跑。默认读 agent/system_prompt.md + niche/<行业>/profile.md。
"""
import os
import requests
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent
NICHE_MAP = {"美业": "beauty", "教培": "education", "电商": "ecommerce", "餐饮": "restaurant"}


def build_prompt(niche_cn: str, customer_msg: str) -> str:
    sys_path = BASE / "agent" / "system_prompt.md"
    niche_path = BASE / "niche" / NICHE_MAP[niche_cn] / "profile.md"
    sys_txt = sys_path.read_text(encoding="utf-8") if sys_path.exists() else ""
    niche_txt = niche_path.read_text(encoding="utf-8") if niche_path.exists() else ""
    return f"{sys_txt}\n\n# 门店资料\n{niche_txt}\n\n# 客户消息\n{customer_msg}"


def call_backend(prompt: str, backend: str) -> str:
    api_map = {
        "openai": ("https://api.openai.com/v1/chat/completions",
                   os.getenv("OPENAI_API_KEY"),
                   {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}),
        "anthropic": ("https://api.anthropic.com/v1/messages",
                      os.getenv("ANTHROPIC_API_KEY"),
                      {"model": "claude-3-5-haiku-latest", "max_tokens": 1024,
                       "messages": [{"role": "user", "content": prompt}]}),
        "xai": ("https://api.x.ai/v1/chat/completions",
                os.getenv("XAI_API_KEY"),
                {"model": "grok-3-mini", "messages": [{"role": "user", "content": prompt}]}),
    }
    url, key, payload = api_map[backend]
    if not key:
        return None
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if backend == "anthropic":
        headers["x-api-key"] = key
        headers["anthropic-version"] = "2023-06-01"
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        data = r.json()
        if backend == "anthropic":
            return "".join(b.get("text", "") for b in data.get("content", []))
        return data["choices"][0]["message"]["content"]
    except Exception as e:  # noqa
        return f"（调用失败：{e}）"


def main():
    st.set_page_config(page_title="AI 销售顾问", layout="centered")
    st.title("AI 销售顾问 · 演示")
    st.caption("输入客户消息，生成【判断】【话术】【节奏】三件套。无 key 时复制提示词去 Grok Bot 跑。")

    niche = st.selectbox("行业", list(NICHE_MAP.keys()))
    backend = st.selectbox("后端（有 key 才生效）", ["auto", "openai", "anthropic", "xai"])
    msg = st.text_area("客户消息", "客户：你们祛痘多少钱？", height=120)

    if st.button("生成", type="primary"):
        full = build_prompt(niche, msg)
        if backend == "auto":
            for b in ("anthropic", "openai", "xai"):
                if os.getenv(f"{b.upper()}_API_KEY"):
                    backend = b
                    break
        out = call_backend(full, backend) if backend != "auto" else None
        if out:
            st.markdown(out)
        else:
            st.warning("没检测到模型 key，下面是拼好的完整提示词，复制去 Grok Bot（免费路由 Claude）跑：")
            st.code(full, language="markdown")


if __name__ == "__main__":
    main()
