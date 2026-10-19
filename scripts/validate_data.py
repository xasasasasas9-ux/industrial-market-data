#!/usr/bin/env python3
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = {
    "category", "province", "city", "date", "price", "priceKind",
    "process", "project", "sourceTitle", "sourceURL",
}

OFFICIAL_HOSTS = {
    "www.ccgp.gov.cn",
    "ccgp.gov.cn",
    "www.ccgp-neimenggu.gov.cn",
    "ccgp-neimenggu.gov.cn",
    "zfcg.henan.gov.cn",
    "erqi.zfcg.henan.gov.cn",
    "shangqiu.zfcg.henan.gov.cn",
    "ggzy.ln.gov.cn",
    "jsggzy.jszwfw.gov.cn",
    "czj.yancheng.gov.cn",
    "lsygcg.com",
    "reportdocs.static.szse.cn",
}

BLOCKED_SOURCE_WORDS = ("新闻", "报道", "媒体", "转载", "公众号")
RESOURCE_WORDS = ("资源化", "热解", "水洗", "熔融", "烧结")
LANDFILL_WORDS = ("填埋", "固化", "稳定化")


def fail(message: str) -> None:
    raise ValueError(message)


def validate(path: Path) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        fail("fly-ash.json 必须是非空数组")

    seen = set()
    current_year = date.today().year
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            fail(f"第 {index} 条不是对象")
        missing = REQUIRED - row.keys()
        if missing:
            fail(f"第 {index} 条缺少字段: {sorted(missing)}")

        category = row["category"]
        if category not in {"resource", "landfill"}:
            fail(f"第 {index} 条 category 无效: {category}")

        if not isinstance(row["price"], (int, float)) or row["price"] <= 0:
            fail(f"第 {index} 条价格无效")

        if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", row["date"]):
            fail(f"第 {index} 条日期格式无效")
        year = int(row["date"][:4])
        if year < 2022 or year > current_year + 1:
            fail(f"第 {index} 条年份超出口径: {year}")

        source_title = row["sourceTitle"]
        if any(word in source_title for word in BLOCKED_SOURCE_WORDS):
            fail(f"第 {index} 条疑似新闻稿或转载来源")

        parsed = urlparse(row["sourceURL"])
        if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_HOSTS:
            fail(f"第 {index} 条来源域名不在正式来源白名单: {parsed.hostname}")

        process = row["process"]
        required_words = RESOURCE_WORDS if category == "resource" else LANDFILL_WORDS
        if not any(word in process for word in required_words):
            fail(f"第 {index} 条工艺无法归入 {category}: {process}")

        if "测算" in row["priceKind"] and "÷" not in source_title:
            fail(f"第 {index} 条测算价缺少金额÷吨数复核口径")

        key = (category, row["province"], row["city"], row["date"], row["project"])
        if key in seen:
            fail(f"第 {index} 条为重复记录: {key}")
        seen.add(key)

    return rows


if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "public/data/v1/fly-ash.json")
    records = validate(target)
    counts = {}
    for record in records:
        key = (record["category"], record["date"][:4])
        counts[key] = counts.get(key, 0) + 1
    print(f"OK: {len(records)} records")
    for key in sorted(counts):
        print(f"  {key[0]} {key[1]}: {counts[key]}")

