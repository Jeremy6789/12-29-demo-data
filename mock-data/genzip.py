import zipfile
import os

output_folder = 'testcases'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def make_noj_zip(zip_filename, cases_list):
    zip_path = os.path.join(output_folder, zip_filename)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        task_idx = 0
        for case_idx, (in_data, out_data) in enumerate(cases_list):
            in_name = f"{task_idx:02d}{case_idx:02d}.in"
            out_name = f"{task_idx:02d}{case_idx:02d}.out"
            zf.writestr(in_name, str(in_data).strip() + "\n")
            zf.writestr(out_name, str(out_data).strip() + "\n")
    print(f"✅ {zip_filename} 產出成功，內含 {len(cases_list)} 組測資。")

# --- 精準測資定義 ---

# C1-1 BMI: 邏輯校正 (H單位: cm)
# 18.5 * (1.7^2) = 53.465, 24 * (1.7^2) = 69.36
bmi_data = [
    ("60 170", "Normal"),       # BMI 20.76
    ("40 160", "Underweight"),  # BMI 15.62
    ("90 180", "Overweight"),   # BMI 27.78
    ("53.465 170", "Normal"),   # BMI 18.5 (邊界)
    ("69.36 170", "Overweight"),# BMI 24.0 (邊界)
    ("50 180", "Underweight")   # BMI 15.43
]

# C1-2 Leap Year
leap_data = [
    ("2000", "Leap Year"), ("1900", "Common Year"), ("2024", "Leap Year"),
    ("2100", "Common Year"), ("1600", "Leap Year"), ("2023", "Common Year")
]

# C1-3 Fibonacci
fib_data = [
    ("0", "0"), ("1", "1"), ("2", "1"), ("10", "55"), ("20", "6765"), ("30", "832040")
]

# C2-1 GCD
gcd_data = [
    ("48 18", "6"), ("101 103", "1"), ("1000 5", "5"), ("123456 789", "3"), ("99 33", "33")
]

# C2-2 Stack
stack_data = [
    ("{[()]}", "Yes"), ("([)]", "No"), ("((()))", "Yes"), ("{", "No"), ("()[]{}", "Yes"), ("(((", "No")
]

# C2-3 Linked List (輸入: 1 2 3 -1 -> 輸出: 3 2 1)
list_data = [
    ("1 2 3 -1", "3 2 1"), 
    ("10 -1", "10"), 
    ("5 4 3 2 1 -1", "1 2 3 4 5"), 
    ("100 200 -1", "200 100")
]

# C3-1 Knapsack (輸入格式: n W \n w v ...)
knap_data = [
    ("3 50\n10 60\n20 100\n30 120", "220"),
    ("1 10\n5 100", "100"),
    ("2 10\n11 50\n12 60", "0") # 全都裝不下
]

# C3-2 LCS
lcs_data = [
    ("ABCBDAB BDCABA", "4"), ("AGGTAB GXTXAYB", "4"), ("AAA BBB", "0"), ("XYZ XYZ", "3")
]

# --- 執行產出 ---
make_noj_zip("c1-1_bmi.zip", bmi_data)
make_noj_zip("c1-2_leap_year.zip", leap_data)
make_noj_zip("c1-3_fibonacci.zip", fib_data)
make_noj_zip("c2-1_gcd.zip", gcd_data)
make_noj_zip("c2-2_stack.zip", stack_data)
make_noj_zip("c2-3_linked_list.zip", list_data)
make_noj_zip("c3-1_knapsack.zip", knap_data)
make_noj_zip("c3-2_lcs.zip", lcs_data)