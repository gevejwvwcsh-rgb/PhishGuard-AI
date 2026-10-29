from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def analyze_url(url):
    url = url.lower()
    score = 0
    reasons = []

    # 1- دومينات مجانية خطيرة
    if re.search(r"\.(tk|ml|ga|cf|gq|xyz|top|buzz)$", url):
        score += 60
        reasons.append("دومين مجاني مشبوه .tk")

    # 2- كلمات تصيد
    if "secure" in url and "facebook" in url:
        score += 70
        reasons.append("انتحال اسم فيسبوك + كلمة secure")

    if "-" in url:
        hyphen_count = url.count("-")
        score += hyphen_count * 15
        reasons.append(f"يوجد {hyphen_count} علامة تصيد - فرطة -")

    if "login" in url or "verify" in url or "account" in url:
        score += 30
        reasons.append("كلمات حساسة: login/verify")

    if len(url) > 30:
        score += 10

    if score >= 50:
        return "موقع تصيد - خطير جدا 🚨", " | ".join(reasons), min(score, 95)
    else:
        return "الموقع يبدو آمن - آمن ✅", "لا يوجد خطر ظاهر 🔍", score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get('url', '')
    pred, reason, score = analyze_url(url)
    return jsonify({"prediction": pred, "reason": reason, "score": score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)