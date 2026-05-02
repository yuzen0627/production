# pip install -U google-generativeai
import google.generativeai as genai

# APIキーの設定（自分のAPIキーに置き換えてください）
genai.configure(api_key="AIzaSyAnli0XBWpbIaYKCpqor4SBDxujZQXfswk")

# モデル選択（安定版）
model = genai.GenerativeModel("gemini-1.5-flash")

# ヒント生成テンプレート
hint_instruction = '''
あなたは学習支援AIです。次の問題に対して、答えを直接言わずにヒントだけを提示してください。
ヒントは100文字以内で、親しみやすく。正確な知識に基づいてください。
'''

# 正誤判定テンプレート
check_instruction = '''
あなたは学習支援AIです。次の問題とユーザーの答えが合っているかを判断してください。
答えは明かさず、合っているかどうかだけを教えてください。
「正しい」「正しくない」だけを短く答えてください。
'''

# 出題と解答のログ
qa_log = {}

while True:
    print("\n=== 新しい問題を始めます ===")
    question = input("問題を入力してください（終了するには「おしまい」と入力） > ").strip()
    if question == "おしまい":
        print("終了します。お疲れさまでした！")
        break

    qa_log["question"] = question

    # 最初のヒント
    prompt = f"{hint_instruction}\n問題: {question}\nヒント:"
    response = model.generate_content(prompt)
    print("AIのヒント:", response.text.strip())

    while True:
        answer = input("あなたの答え > ").strip()
        qa_log["answer"] = answer

        # 正誤判定
        prompt_check = f"{check_instruction}\n問題: {qa_log['question']}\nユーザーの答え: {qa_log['answer']}\n判定:"
        response_check = model.generate_content(prompt_check)
        judgment = response_check.text.strip().lower()

        if "正しい" in judgment:
            print("AIの判定: 正解です！よくできました👏")
            break
        else:
            print("AIの判定: うーん、まだ違うよ。もう一つヒントをあげるね。")
            prompt_hint = f"{hint_instruction}\n問題: {qa_log['question']}\nヒント:"
            response_hint = model.generate_content(prompt_hint)
            print("追加ヒント:", response_hint.text.strip())
