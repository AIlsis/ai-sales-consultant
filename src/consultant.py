#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 销售顾问 · 最小可运行版（多后端，不锁死任何一家）

支持后端：xAI(Grok) / Anthropic(Claude) / OpenAI
自动按环境变量里存在的 key 选后端，也可 BACKEND=xxx 强制。

用法：
  pip install requests
  export ANTHROPIC_API_KEY=sk-ant-...      # 或 OPENAI_API_KEY / XAI_API_KEY
  python src/consultant.py "客户：你们祛痘多少钱？"
  echo "客户：问完价格没回" | python src/consultant.py
"""
import os
import sys

import requests

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    p = os.path.join(REPO, path)
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as f:
        return f.read()


SYSTEM = load("agent/system_prompt.md")
NICHE = load("niche/beauty/profile.md")


def build_system():
    s = SYSTEM
    if NICHE:
        s += "\n\n# 门店资料（长期记忆）\n" + NICHE
    return s


def pick_backend():
    forced = os.getenv("BACKEND")
    if forced:
        return forced
    if os.getenv("XAI_API_KEY"):
        return "xai"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return None


def call_openai(system, user):
    key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "system", "content": system},
                                            {"role": "user", "content": user}], "temperature": 0.7},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def call_xai(system, user):
    key = os.getenv("XAI_API_KEY")
    model = os.getenv("XAI_MODEL", "grok-4-latest")
    r = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "system", "content": system},
                                            {"role": "user", "content": user}], "temperature": 0.7},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def call_anthropic(system, user):
    key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
        json={"model": model, "max_tokens": 1024, "system": system,
              "messages": [{"role": "user", "content": user}]},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"]


DISPATCH = {"openai": call_openai, "anthropic": call_anthropic, "xai": call_xai}


def main():
    backend = pick_backend()
    if not backend:
        print("没检测到 API key。请设置 XAI_API_KEY / ANTHROPIC_API_KEY / OPENAI_API_KEY 之一。")
        sys.exit(1)
    if len(sys.argv) > 1:
        user = " ".join(sys.argv[1:])
    else:
        user = sys.stdin.read().strip()
    if not user:
        print('用法：python src/consultant.py "客户消息..."')
        sys.exit(1)
    print(f"[后端] {backend}\n")
    out = DISPATCH[backend](build_system(), user)
    print(out)


if __name__ == "__main__":
    main()
