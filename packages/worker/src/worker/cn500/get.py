import json
import pandas as pd

df = pd.read_csv("~/Downloads/000905cons.csv")
print(df.head(5))


# 假设你的 DataFrame 变量名是 df
# df = ...

code_col = "成份券代码Constituent Code"
name_col = "成份券名称Constituent Name"

# 生成 dict list
records = df[[code_col, name_col]].copy()


# 成份券代码补齐 6 位（先处理 NaN / 浮点显示等情况）
def to_6d_code(x) -> str:
  if pd.isna(x):
    return ""
  # 避免 9.0 这种浮点形式带来的 '.0'
  s = str(int(x)) if isinstance(x, (int, float)) and float(x).is_integer() else str(x)
  s = s.strip()
  # 若仍可能出现 '9.0'，再兜底一次
  if s.endswith(".0"):
    s = s[:-2]
  return s.zfill(6)


records["stock_code"] = records[code_col].apply(to_6d_code)
records["stock_name"] = records[name_col].astype(str)

out = records[["stock_code", "stock_name"]].to_dict(orient="records")

# 写入 ./cn500.json
with open("./cn500.json", "w", encoding="utf-8") as f:
  json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Saved {len(out)} records to ./cn500.json")
