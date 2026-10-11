# ai-sales-consultant · AI 销售顾问（开源版）

零代码起步、可本地运行、可一键部署的 AI 销售顾问模板。把「会说话的店长」固化成提示词 + 工作流，帮**美业 / 教培 / 电商 / 餐饮**门店做私域转化、客户分层和自动跟单。

> 设计原则：**不锁死任何一家模型**。默认走 Grok（免费路由 Claude），本地运行版支持 OpenAI / Anthropic / xAI 多后端，哪家有 key 用哪家。

## 免费版 vs 付费进阶包

| | 免费版（本仓库）| 付费进阶包 ¥39–99 |
|---|---|---|
| 覆盖行业 | 美业 | 美业 + 教培 + 电商 + 餐饮 全套 |
| 话术模板 | 4 套基础场景 | 每行业 6+ 套分场景话术 |
| 运行方式 | 本地脚本 / Grok Bot | 附 Web 演示页（Streamlit）|
| 部署 | 自己折腾 | 一键部署教程 + 视频 |
| 支持 | README + issue | 私域答疑群 |

付费包挂 Gumroad，买了自动发，**不靠任何内容号引流**——项目被搜到靠 GitHub 搜索和 awesome 列表，转化发生在产品页里。

## 快速开始（本地）

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

无 key 也能用：把需求丢进 **Grok Bot**（让它路由到 Claude Opus），系统提示词在 `agent/system_prompt.md`，行业资料在 `niche/`。

## 一键部署（可选 · 带返佣）

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app?referralCode=你的返佣码)

点按钮用 Railway 一键部署 Web 演示页，**别人部署你拿 affiliate 返佣**。把 `你的返佣码` 换成自己的 Railway referral 码即可。

## 目录结构

```
ai-sales-consultant/
├─ README.md                # 本文件
├─ PREMIUM.md               # 付费进阶包说明 + 购买链接
├─ agent/
│  └─ system_prompt.md      # 销售顾问系统提示词（核心）
├─ workflows/
│  └─ routines.md           # Grok Bot 的 24h 自动工作流
├─ prompts/                 # 分场景话术模板（美业，可直接抄）
│  ├─ 01_首咨.md
│  ├─ 02_价格异议.md
│  ├─ 03_催到店.md
│  └─ 04_办卡回购.md
├─ niche/                   # 各行业的门店资料模板（喂 Agent 当长期记忆）
│  ├─ beauty/        profile.md
│  ├─ education/     profile.md   # 教培
│  ├─ ecommerce/     profile.md   # 电商
│  └─ restaurant/    profile.md   # 餐饮
├─ examples/
│  └─ diagnostic_case.md    # 一个脱敏诊断案例
├─ app.py                   # 一键部署用的 Web 演示页（Streamlit）
├─ src/
│  └─ consultant.py         # 最小可运行脚本（多后端）
├─ requirements.txt
└─ .env.example
```

## 怎么变现（产品型开源，不引流）

不需要发抖音 / 小红书做号，靠产品本身转化：

1. **GitHub Sponsors / 爱发电**：README 挂赞助入口，用的人直接月捐。
2. **卖付费包**：Gumroad 挂进阶版（多行业 + Web 演示 + 部署教程），被动收入。
3. **部署返佣**：上面的 Railway 按钮，有人部署你吃分成。
4. **被动曝光**：提交到 `awesome-ai-agents`、`awesome-chatgpt-prompts` 等列表，AI agent 类现在搜索量大，自然来人。

> 你只管把项目做好、被人搜到，转化发生在产品页里，不用你主动发一条笔记。

## 支持这个项目

- GitHub Sponsors：https://github.com/sponsors/AIlsis
- 爱发电（中文，主推）：https://afdian.com/a/_bead8
- 付费进阶包：爱发电挂付费内容（中文，推荐）或 Gumroad（英文）：https://yourname.gumroad.com/l/ai-sales-consultant

（Sponsors 已填你的 GitHub 名 AIlsis；爱发电 ID 换成你自己的，去 afdian.com 注册即得。Gumroad / Railway 是英文平台，嫌麻烦可先不弄，不影响爱发电变现。）

## 推荐工具（affiliate 返佣）

如果你用下面工具部署或体验本项目，从我的链接注册，我能拿到佣金（你的价格不变）：

- [Cursor](https://cursor.com/你的referral) — AI 代码编辑器（写提示词、改脚本）
- [Vercel](https://vercel.com/你的referral) — 一键部署本项目演示页 app.py
- [Railway](https://railway.app/?ref=你的referral) — 云部署，也跑本项目
- [腾讯云](https://cloud.tencent.com/referral?inviter=你的ID) — 国内云算力 / 部署
- [阿里云](https://www.aliyun.com/你的affiliate) — 国内云服务器

> 把上面的「你的referral / 你的ID / 你的affiliate」换成你在各平台 affiliate / referral 计划的专属链接即可。有人点进去注册，你就拿佣金——零运营、纯被动，和这个仓库天然配合。

## 许可证

MIT —— 随便用、随便改、商用也行，留个署名就好。

## 免责声明

- 客户聊天记录、手机号等敏感信息请脱敏后再喂模型；
- 本项目是工具模板，不对使用结果负责，商用前请自行评估合规。
