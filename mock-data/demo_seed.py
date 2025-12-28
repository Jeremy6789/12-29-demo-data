import sys
import os
from datetime import datetime, timedelta
from mongoengine import connect, disconnect_all

# 確保路徑正確，以便匯入 mongo 模組
sys.path.append(os.getcwd())

# 1. 斷開既存連線並重新連線至 Docker 環境
disconnect_all()
try:
    # 根據 NOJ 預設，資料庫名稱通常為 'normal-oj'
    connect('normal-oj', host='mongodb://localhost:27017')
    print("✅ 已成功連接至真實 MongoDB (Docker)")
except Exception as e:
    print(f"❌ 連接失敗: {e}")
    sys.exit(1)

# 2. 匯入模型與引擎
from mongo import User, Course, Problem, Homework, Announcement, engine

# --- 詳細題目敘述庫 (使用 r 前綴確保 LaTeX 反斜線不被轉義) ---

D_BMI = r"""## 任務描述
請撰寫一個程式，讀取使用者的體重 (kg) 與身高 (cm)，並計算其 BMI 值。
公式如下：$BMI = weight(kg) / height^2(m)$

## 判定標準
- $BMI < 18.5$: 輸出 `Underweight`
- $18.5 \le BMI < 24$: 輸出 `Normal`
- $BMI \ge 24$: 輸出 `Overweight`

## 範例輸入
65.5 175.0

## 範例輸出
Normal

"""

D_LEAP = r"""## 任務描述
判斷輸入年份 $Y$ 是否為閏年。

## 判斷規則
1. 年份若能被 400 整除，則為閏年。
2. 若年份能被 4 整除但「不能」被 100 整除，亦為閏年。
3. 其餘年份皆為平年 (`Common Year`)。

## 範例輸入
2024

## 範例輸出
Leap Year

"""

D_FIBO = r"""## 任務描述
計算費氏數列的第 $n$ 項。
定義：$F(0)=0, F(1)=1$，且對於 $n \ge 2$，$F(n) = F(n-1) + F(n-2)$。

## 限制
- $0 \le n \le 30$
- 時間限制：1.0s
"""

D_GCD = r"""## 任務描述
使用「輾轉相除法」計算兩個正整數 $a, b$ 的最大公因數 (GCD)。

## 限制
$1 \le a, b \le 2^{31}-1$
"""

D_STACK = r"""## 任務描述
利用 **Stack (堆疊)** 資料結構判斷括號對齊是否合法。
包含：小括號 `()`、中括號 `[]`、大括號 `{}`。

## 判定規則
- 左括號必須以正確的順序閉合（先入後出）。
"""

D_LL = r"""## 任務描述
給定一個單向鏈表，實作原地 (In-place) 反轉鏈表的演算法。
**注意：** 要求交換指標邏輯，非僅反向輸出數值。
"""

D_KNAP = r"""## 任務描述
經典 0/1 背包問題。給定 $N$ 件物品的重量與價值，在負重上限 $W$ 內，求最大價值總和。

## 限制
$N \le 100, W \le 1000$
"""

D_LCS = r"""## 任務描述
找出兩組字串中最長公共子序列 (Longest Common Subsequence) 的長度。
"""

def seed():
    print("🎓 正在執行「Public 模式 + 自動清理」匯入程序...")
    try:
        # --- 0. 獲取底層 Collection 用於強制操作 ---
        user_col = engine.User._get_collection()
        course_col = engine.Course._get_collection()
        problem_col = engine.Problem._get_collection()
        ann_col = engine.Announcement._get_collection()
        hw_col = engine.Homework._get_collection()

        # --- 1. 深度清理 (防止重複 ID 與舊數據殘留) ---
        print("-> 正在清理舊有的 Demo 資料...")
        demo_usernames = ["prof_wang"] + [f"411470{i:02d}S" for i in range(1, 11)]
        user_col.delete_many({"_id": {"$in": demo_usernames}})
        
        c_names = ["Public", "CS101_Computer_Programming", "CS201_Data_Structures", "CS301_Algorithms"]
        course_col.delete_many({"courseName": {"$in": c_names}})
        problem_col.delete_many({"problemId": {"$in": list(range(101, 115))}})
        ann_col.delete_many({"title": {"$regex": "重要|MOSS"}})
        hw_col.delete_many({"hwName": {"$regex": "Week 3"}})

        # --- 2. 建立角色 ---
        print("-> 重新建立教授與學生帳號...")
        prof_wrapper = User.signup("prof_wang", "pass123", "wang@ntnu.edu.tw").activate()
        u_doc = engine.User.objects(username="prof_wang").first()
        u_doc.role = 1 # 教授
        u_doc.save()

        for i in range(1, 11):
            uid = f"411470{i:02d}S"
            User.signup(uid, "student123", f"{uid}@ntnu.edu.tw").activate()

        # --- 3. 建立課程 (必須先有 Public) ---
        print("-> 建立 Public 及學期課程...")
        course_map = {}
        for name in c_names:
            Course.add_course(name, "prof_wang")
            co_obj = engine.Course.objects(course_name=name).first()
            if name != "Public":
                # 將學生加入對應課程
                Course(name).update_student_namelist({f"411470{i:02d}S": f"學生{i}" for i in range(1, 11)})
            course_map[name] = co_obj

        # --- 4. 建立題目 (核心修復：全部歸屬 Public 課程) ---
        print("-> 正在將 8 個題目匯入 Public 區並補全渲染欄位...")
        p_data = [
            ("BMI計算機", ["Python3"], D_BMI, 6),
            ("閏年判斷", ["Python3"], D_LEAP, 4),
            ("費氏數列", ["Python3", "C++"], D_FIBO, 5),
            ("最大公因數(GCD)", ["C", "C++"], D_GCD, 4),
            ("合法括號匹配", ["C++"], D_STACK, 4),
            ("鏈表反轉", ["C"], D_LL, 4),
            ("0/1背包問題", ["C++"], D_KNAP, 2),
            ("最長公共子序列", ["C++"], D_LCS, 3)
        ]

        for i, (title, langs, desc, count) in enumerate(p_data):
            p_id = 101 + i
            # 使用字典格式直接寫入，確保欄位名稱與資料庫結構絕對一致
            doc = {
                "problemId": p_id,
                "problemName": title,
                "description": desc,
                "owner": u_doc.pk,
                "courses": [course_map["Public"].pk], # 關鍵：屬於 Public
                "problemStatus": 0,
                "problemType": 0,
                "allowedLanguage": langs,
                "quota": -1,
                "testCase": {
                    "tasks": [{
                        "caseCount": count,
                        "taskScore": 100,
                        "memoryLimit": 64 * 1024 * 1024,
                        "timeLimit": 1000
                    }]
                },
                "tags": ["Public", "University"],
                "canViewStdout": True,
                "acUser": 0,
                "submitter": 0
            }
            problem_col.update_one({"problemId": p_id}, {"$set": doc}, upsert=True)

        # --- 5. 建立公告與作業 ---
        print("-> 建立擬真公告與學期作業...")
        Announcement.new_ann(
            title="【重要】關於 MOSS 程式抄襲偵測之聲明",
            creator=u_doc,
            markdown="本學期作業將使用 **MOSS** 比對。題目已發布於 Public 區，請同學獨立完成。",
            pinned=True,
            course="Public"
        )

        Homework.add(
            user=u_doc,
            course_name="CS101_Computer_Programming",
            hw_name="Week 3：基礎語法練習任務",
            markdown="請前往題目列表完成「BMI計算機」與「閏年判斷」。",
            start=datetime.now() - timedelta(days=1),
            end=datetime.now() + timedelta(days=7),
            problem_ids=[101, 102],
            scoreboard_status=0
        )

        print("\n✅ [成功] 擬真資料匯入完成！")
        print("💡 題目現在全部位於 Public 區。")
        print("🔑 教授帳號: prof_wang / pass123")

    except Exception as e:
        import traceback
        print(f"\n❌ [錯誤] 匯入失敗: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    seed()