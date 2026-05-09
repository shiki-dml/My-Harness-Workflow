# Release Readiness Harness

**语言:** [English](README.md) | 中文

这个 harness 的场景来源于公开的 [FastAPI](https://github.com/fastapi/fastapi)
项目。FastAPI 是基于 Starlette 和 Pydantic 的生产级 Python API framework，
因此适合模拟依赖升级、CI 矩阵、兼容性、文档和发布门禁检查。

## 用途

该 harness 会把离线 release manifest 转换成 release readiness report：
dependency graph、change registry、release backlog、risk ledger、release
contract、implementation plan、test strategy、QA result 和 handoff summary。

## 运行

```powershell
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72 --json
```

## 使用的 Agents

1. `human_steering` 定义发布边界和风险预算。
2. `harness_orchestrator` 固定阶段顺序。
3. `initializer_agent` 校验并标准化 manifest。
4. `repo_cartographer` 映射 fixture 和源项目。
5. `feature_registry_curator` 创建 change registry。
6. `product_planner` 根据风险和 blocker 状态排序发布变更。
7. `sprint_contract_agent` 构建 release contract。
8. `implementation_generator` 创建范围明确的发布动作。
9. `test_strategist` 创建验证矩阵。
10. `qa_evaluator` 检查发布 invariants。
11. `handoff_writer` 汇总 readiness 和下一步归属。

