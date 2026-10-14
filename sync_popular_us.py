# sync_popular_us.py
import json

with open("stocks_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

with open("all_global_stocks_compact.json", "r", encoding="utf-8") as f:
    compact = json.load(f)

us_map = {}
for s in db.get("us", []):
    us_map[s["code"].upper()] = s

US_POPULAR_DICT = {
    "SPCX": ("스페이스X", 156.54, -4.21, -6.88),
    "NVDA": ("엔비디아", 138.25, 3.15, 4.22),
    "TSLA": ("테슬라", 218.85, 2.40, 5.12),
    "AAPL": ("애플", 232.10, 0.85, 1.95),
    "MSFT": ("마이크로소프트", 418.50, 1.12, 4.65),
    "AMZN": ("아마존", 186.40, 1.45, 2.67),
    "GOOGL": ("구글 알파벳 A", 165.30, 0.64, 1.05),
    "GOOG": ("구글 알파벳 C", 166.80, 0.58, 0.96),
    "META": ("메타 (페이스북)", 582.10, 2.80, 15.85),
    "TSM": ("TSMC", 190.20, 4.10, 7.50),
    "PLTR": ("팔란티어", 43.50, 5.40, 2.23),
    "AMD": ("AMD", 155.80, 2.30, 3.50),
    "INTC": ("인텔", 22.40, -1.15, -0.26),
    "NFLX": ("넷플릭스", 705.20, 1.90, 13.15),
    "COIN": ("코인베이스", 195.40, 3.80, 7.15),
    "AVGO": ("브로드컴", 178.60, 2.10, 3.68),
    "QCOM": ("퀄컴", 168.30, 1.25, 2.08),
    "SMCI": ("슈퍼마이크로컴퓨터", 48.20, 6.50, 2.94),
    "ARM": ("ARM 홀딩스", 142.50, 3.20, 4.42),
    "UBER": ("우버", 78.50, 1.85, 1.42),
    "BRK.B": ("버크셔 해서웨이 B", 452.30, 0.45, 2.02),
    "BRK.A": ("버크셔 해서웨이 A", 682500.0, 0.40, 2730.0),
    "DIS": ("월트 디즈니", 95.80, 0.80, 0.76),
    "NKE": ("나이키", 82.40, -0.60, -0.50),
    "SBUX": ("스타벅스", 96.20, 0.35, 0.34),
    "BABA": ("알리바바", 101.50, 2.15, 2.14),
    "SONY": ("소니", 18.90, 0.75, 0.14),
    "RIVN": ("리비안", 10.45, 1.80, 0.18),
    "LCID": ("루시드", 3.25, 2.10, 0.07),
    "IONQ": ("아이온큐", 12.80, 8.40, 0.99),
    "SOUN": ("사운드하운드 AI", 5.12, 4.30, 0.21),
    "RGTI": ("리게티 컴퓨팅", 1.45, 5.20, 0.07),
    "ACU": ("아크메 유나이티드", 38.40, 1.20, 0.46),
    "SVM": ("실버코프 메탈스", 3.85, -0.50, -0.02),
}

updated_count = 0
for row in compact:
    code = row[0].upper()
    if code in US_POPULAR_DICT:
        kr_name, price, change, diff = US_POPULAR_DICT[code]
        row[3] = price
        row[4] = change
        row[5] = diff
        if len(row) <= 6:
            row.append(kr_name)
        else:
            row[6] = kr_name
        updated_count += 1
    elif code in us_map:
        us_obj = us_map[code]
        if us_obj.get("price") and us_obj["price"] != 100.0:
            row[3] = us_obj["price"]
            row[4] = us_obj.get("change", 0.0)
            row[5] = us_obj.get("diff", 0.0)
            kr_cand = us_obj.get("krName") or us_obj.get("name", "").split(" (")[0]
            if len(row) <= 6:
                row.append(kr_cand)
            else:
                row[6] = kr_cand
            updated_count += 1

print(f"Updated {updated_count} US popular stocks in compact json!")

with open("all_global_stocks_compact.json", "w", encoding="utf-8") as f:
    json.dump(compact, f, ensure_ascii=False)

print("Successfully saved all_global_stocks_compact.json!")
