# 工业品行情统一数据服务

为 macOS「工业品行情」和 Android/EMUI 桌面组件提供同一份只读公开数据。

## 在线数据

- `public/data/v1/manifest.json`：版本、更新时间、记录数与 SHA-256。
- `public/data/v1/fly-ash.json`：飞灰资源化与稳定化后填埋价格。
- `public/data/v1/sources.json`：当前正式来源域名清单。
- `candidates/pending.json`：尚未通过口径核验的候选记录，不对客户端发布。

发布地址：

`https://xasasasasas9-ux.github.io/industrial-market-data/data/v1/manifest.json`

## 数据准入

仅接受政府采购网、公共资源交易平台、正式招标/中标/合同附件，以及用于复核招投标数据的正式监管披露文件。排除新闻稿、行业媒体、转载、无法回溯原件的数据，以及工艺不明确的“综合处置”项目。

- `resource`：必须明确属于热解、水洗、熔融、烧结或其他资源化利用。
- `landfill`：必须明确属于固化/稳定化后的填埋处置。
- 单位统一为人民币元/吨。
- 测算价必须在来源标题中保留可复核的金额÷吨数口径。

## 本地验证

```bash
python3 scripts/validate_data.py public/data/v1/fly-ash.json
python3 scripts/build_manifest.py public/data/v1/fly-ash.json public/data/v1/manifest.json
```

GitHub Actions 会在每次提交、手动运行和每月1日09:00（Asia/Shanghai）执行相同验证，并在通过后发布 GitHub Pages。

