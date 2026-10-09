# ai-sales-consultant · AI 销售顾问（开源版）

一个**零代码起步、可本地运行**的 AI 销售顾问模板。把「会说话的店长」固化成提示词 + 工作流，帮美业/教培/本地生活门店做私域转化、客户分层和自动跟单。

> 设计原则：**不锁死任何一家模型**。默认走 Grok（免费路由 Claude），本地运行版支持 OpenAI / Anthropic / xAI 多后端，哪家有 key 用哪家。

## 它解决啥

门店不是没客人，是客人在私信里聊着聊着就凉了。这个项目把「首咨 → 价格异议 → 催到店 → 办卡回购」的话术和跟单节奏固化下来，老板不用守手机也能接住每一个咨询。

## 快速开始

```bash
git clone <你的仓库地址>
cd ai-sales-consultant
pip install -r requirements.txt

# 配一个后端 key（三选一）
export ANTHROPIC_API_KEY=sk-ant-...     # 或 OPENAI_API_KEY / XAI_API_KEY

# 跑起来
python src/consultant.py "客户：你们祛痘多少钱？"
echo "客户：问完价格没回" | python src/consultant.py
```

强制指定后端：`BACKEND=openai python src/consultant.py "..."`

## 目录结构

```
ai-sales-consultant/
├─ README.md                # 本文件
├─ agent/
│  └─ system_prompt.md      # 销售顾问的系统提示词（核心）
├─ workflows/
│  └─ routines.md           # Grok Bot 的 24h 自动工作流
├─ prompts/                 # 分场景话术模板（可直接抄）
│  ├─ 01_首咨.md
│  ├─ 02_价格异议.md
│  ├─ 03_催到店.md
│  └─ 04_办卡回购.md
├─ niche/
│  └─ beauty/
│     └─ profile.md         # 美业门店资料模板（项目/价格/常见问题）
├─ examples/
│  └─ diagnostic_case.md    # 一个脱敏诊断案例
├─ src/
│  └─ consultant.py         # 最小可运行脚本（多后端）
├─ requirements.txt
└─ .env.example
```

## 怎么变现（开源 → 引流 → 卖服务）

1. 发 repo，写「我做开源 AI 销售顾问的复盘」蹭 AI 资讯流量；
2. 美业老板/AI 玩家来 star、fork，变成你的获客漏斗；
3. 顺手卖：搭建费（¥800–2000）+ 月费代运营（¥500–1500），或按成交额抽 3–5%。

> 开源是「卖服务」的放大器 + 护城河：先攒信任和流量，再转化付费客户。

## 许可证

MIT —— 随便用、随便改、商用也行，留个署名就好。

## 免责声明

- 客户聊天记录、手机号等敏感信息请脱敏后再喂模型；
- 本项目是工具模板，不对使用结果负责，商用前请自行评估合规。
