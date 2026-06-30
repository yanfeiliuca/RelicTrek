# 女娲技能库 · Nuwa Skills Library

> 蒸馏自人类智慧大师的可调用AI思维技能集合

## 什么是女娲技能库

女娲技能库是一套结构化的AI思维技能规范，旨在将人类历史上卓越思想家、企业家、战略家的思维模式提炼为机器可读、AI可调用的格式，让任何AI系统在面临特定挑战时能够主动激活相应的人类智慧。

## 使用方式

### AI调用协议

当AI系统面临与某个技能的 `activation_triggers` 匹配的场景时，应：

1. 加载对应技能的 `thinking_patterns`
2. 按 `decision_framework.steps` 的顺序过滤决策思路
3. 选择最匹配当前场景的 `application_scenarios` 及其 `recommended_patterns`
4. 输出时标注：「以 [技能名称] 视角分析：」

### 技能索引

见 `registry.json`。

## 已收录技能

| 技能ID | 人物 | 领域 | 核心模式数 |
|--------|------|------|-----------|
| `nuwa.entrepreneurship.yu-minhong` | 俞敏洪 | 创业·教育 | 6 |

## 技能格式规范

见 `schema.json`（JSON Schema Draft-07）。

### 核心字段

- **thinking_patterns**: 提炼的思维模式列表，每条包含：
  - `mechanism`: 输入→处理步骤→输出的完整机制
  - `examples`: 真实历史案例验证
  - `anti_patterns`: 应避免的反面思维
- **decision_framework**: 按此人视角做决策的步骤流程
- **activation_triggers**: AI自动匹配此技能的场景关键词
- **compatibility**: 与其他技能的协同与冲突关系

## 蒸馏质量标准

每一条技能收录必须满足：

1. **可证伪性** — 思维模式须有真实历史事件作为例证，不接受纯理论描述
2. **可操作性** — `mechanism.process` 必须是AI可执行的具体步骤，而非模糊原则
3. **反模式标注** — 每个模式须标注典型的错误应用方式
4. **跨域迁移性** — `application_scenarios` 须覆盖原始人物领域之外的通用场景

## 贡献新技能

新技能需满足 `schema.json` 的全部必填字段，并在 `registry.json` 中注册后方可生效。
