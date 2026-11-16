import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import math
import os
from datetime import datetime

# 1. 타로 카드 21장 데이터 (문양 타입 symbol_type 및 고유 테마 색상 포함)
TAROT_CARDS = {
    1: {
        "roman": "I", "symbol": "✦", "color": "#4A154B",
        "name": "1. 마법사", "eng": "The Magician", "keyword": "창조와 새로운 시작",
        "event": "자신의 숨겨진 재능을 발휘해 새로운 일이나 프로젝트를 주도적으로 시작하는 일",
        "advice": "머릿속으로만 생각하던 계획을 실행에 옮기면 기대 이상의 성과를 거두게 됩니다."
    },
    2: {
        "roman": "II", "symbol": "☾", "color": "#1D3557",
        "name": "2. 여사제", "eng": "The High Priestess", "keyword": "지혜와 문서운",
        "event": "깊은 통찰력을 얻어 중요한 시험에 합격하거나 유리한 계약·문서를 손에 쥐는 일",
        "advice": "주변의 말에 흔들리지 말고 본인의 직관과 냉철한 판단력을 믿는 것이 좋습니다."
    },
    3: {
        "roman": "III", "symbol": "♛", "color": "#2D6A4F",
        "name": "3. 여황제", "eng": "The Empress", "keyword": "풍요와 결실",
        "event": "그동안 투자한 노력과 시간이 물질적·정신적 풍요로 돌아와 여유를 누리는 일",
        "advice": "주변 사람들에게 베풀수록 더 큰 복과 재물이 되어 돌아오는 시기입니다."
    },
    4: {
        "roman": "IV", "symbol": "♚", "color": "#6A040F",
        "name": "4. 황제", "eng": "The Emperor", "keyword": "권위와 안정",
        "event": "조직이나 모임에서 리더십을 인정받아 높은 자리로 올라서거나 기반을 확고히 다지는 일",
        "advice": "책임감을 가지고 원칙대로 밀고 나가면 아무도 당신의 자리를 흔들 수 없습니다."
    },
    5: {
        "roman": "V", "symbol": "✞", "color": "#582F0E",
        "name": "5. 교황", "eng": "The Hierophant", "keyword": "귀인과 조언",
        "event": "인생의 멘토나 뜻밖의 귀인을 만나 막혀 있던 문제를 해결하고 올바른 길을 찾는 일",
        "advice": "혼자 고민하기보다 경험 많은 연장자나 전문가의 조언을 적극적으로 수용하세요."
    },
    6: {
        "roman": "VI", "symbol": "♥", "color": "#800F2F",
        "name": "6. 연인", "eng": "The Lovers", "keyword": "인연과 파트너십",
        "event": "운명적인 연인을 만나거나 마음이 완벽히 통하는 최고의 동업자·파트너를 얻는 일",
        "advice": "인간관계에서 오는 기쁨이 크지만, 중요한 순간에는 감정에 휩쓸리지 않는 선택이 필요합니다."
    },
    7: {
        "roman": "VII", "symbol": "▲", "color": "#1B4332",
        "name": "7. 전차", "eng": "The Chariot", "keyword": "돌파와 승리",
        "event": "강한 추진력으로 경쟁자를 물리치고 원하던 목표를 향해 빠르게 돌진해 성취하는 일",
        "advice": "망설임은 금물입니다. 목표가 정해졌다면 뒤를 돌아보지 말고 과감하게 전진하세요."
    },
    8: {
        "roman": "VIII", "symbol": "∞", "color": "#7F4F24",
        "name": "8. 힘", "eng": "Strength", "keyword": "인내와 내면의 힘",
        "event": "어려운 상황이나 까다로운 사람을 부드러운 카리스마와 끈기로 완벽히 내 편으로 만드는 일",
        "advice": "강압적인 태도보다는 포용력과 인내심이 결국 더 큰 승리를 가져다줍니다."
    },
    9: {
        "roman": "IX", "symbol": "❖", "color": "#2B2D42",
        "name": "9. 은둔자", "eng": "The Hermit", "keyword": "성찰과 탐구",
        "event": "잠시 주변의 소음에서 벗어나 혼자만의 연구나 준비 끝에 독보적인 전문성을 갖추는 일",
        "advice": "당장 눈에 보이는 결과에 조급해하지 말고 내실을 다지는 시간으로 삼으세요."
    },
    10: {
        "roman": "X", "symbol": "◎", "color": "#3C096C",
        "name": "10. 운명의 수레바퀴", "eng": "Wheel of Fortune", "keyword": "전환점과 행운",
        "event": "예상치 못한 우연한 기회를 통해 인생의 흐름이 긍정적인 방향으로 크게 뒤바뀌는 일",
        "advice": "변화의 파도가 찾아올 때 두려워하지 말고 흐름에 몸을 맡기면 행운이 따릅니다."
    },
    11: {
        "roman": "XI", "symbol": "◈", "color": "#003049",
        "name": "11. 정의", "eng": "Justice", "keyword": "공정함과 보상",
        "event": "공정한 평가를 통해 그동안의 노력에 대한 정당한 대가나 법적·사회적 승리를 얻는 일",
        "advice": "감정을 배제하고 이성적이고 균형 잡힌 태도를 유지할 때 가장 큰 이득을 봅니다."
    },
    12: {
        "roman": "XII", "symbol": "▼", "color": "#3D405B",
        "name": "12. 매달린 사람", "eng": "The Hanged Man", "keyword": "관점의 전환",
        "event": "잠시 정체기를 겪는 듯하나 고정관념을 깨는 발상의 전환으로 새로운 돌파구를 찾는 일",
        "advice": "더 큰 도약을 위해 잠시 숨을 고르는 시기이니, 시야를 넓혀 다른 각도에서 문제를 바라보세요."
    },
    13: {
        "roman": "XIII", "symbol": "❂", "color": "#212529",
        "name": "13. 죽음", "eng": "Death", "keyword": "종결과 새출발",
        "event": "나를 힘들게 하던 과거의 인연이나 해묵은 문제를 완전히 정리하고 새로운 인생 2막을 여는 일",
        "advice": "끝은 곧 새로운 시작을 의미합니다. 지나간 것에 미련을 두지 말아야 새 행운이 들어옵니다."
    },
    14: {
        "roman": "XIV", "symbol": "☯", "color": "#005F73",
        "name": "14. 절제", "eng": "Temperance", "keyword": "조화와 균형",
        "event": "서로 다른 영역이나 의견을 조화롭게 융합하여 안정적이고 평화로운 환경을 만드는 일",
        "advice": "무리한 욕심을 부리기보다 현재 가진 것들의 균형을 맞추며 순리대로 나아가는 것이 좋습니다."
    },
    15: {
        "roman": "XV", "symbol": "ψ", "color": "#590D22",
        "name": "15. 악마", "eng": "The Devil", "keyword": "강한 매혹과 집념",
        "event": "특정 분야에 무섭게 몰입하여 큰 금전적 이득을 얻거나 치명적인 매력으로 사람을 끌어당기는 일",
        "advice": "큰 쾌락이나 금전운이 따르지만, 과욕이나 유혹에 빠져 통제력을 잃지 않도록 주의해야 합니다."
    },
    16: {
        "roman": "XVI", "symbol": "⚡", "color": "#370617",
        "name": "16. 탑", "eng": "The Tower", "keyword": "급격한 변화와 각성",
        "event": "기존의 틀을 깨부수는 갑작스러운 사건을 계기로 잘못된 기반을 허물고 처음부터 제대로 다시 세우는 일",
        "advice": "예상치 못한 변화에 당황할 수 있으나, 이는 더 튼튼한 미래를 짓기 위한 액땜과 같습니다."
    },
    17: {
        "roman": "XVII", "symbol": "★", "color": "#1E3A8A",
        "name": "17. 별", "eng": "The Star", "keyword": "희망과 인기운",
        "event": "많은 사람의 주목과 사랑을 받으며 오랫동안 꿈꿔오던 이상에 한 걸음 다가서는 일",
        "advice": "당신의 존재감이 빛을 발하는 시기이니, 긍정적인 마음으로 자신을 널리 드러내세요."
    },
    18: {
        "roman": "XVIII", "symbol": "☽", "color": "#312E81",
        "name": "18. 달", "eng": "The Moon", "keyword": "감수성과 이면의 발견",
        "event": "남들이 보지 못하는 숨겨진 진실을 파악하거나 예술적·창의적 영감이 폭발하는 일",
        "advice": "막연한 불안감에 흔들리지 말고, 안개가 걷힐 때까지 신중하게 상황을 관찰하세요."
    },
    19: {
        "roman": "XIX", "symbol": "☀", "color": "#9A3412",
        "name": "19. 태양", "eng": "The Sun", "keyword": "성공과 활력",
        "event": "모든 장애물이 사라지고 하는 일마다 밝은 빛을 보며 주위의 축복 속에 큰 성공을 거두는 일",
        "advice": "인생의 황금기 중 하나입니다. 숨김없이 당당하게 행동할수록 모든 운이 당신을 돕습니다."
    },
    20: {
        "roman": "XX", "symbol": "♪", "color": "#4C1D95",
        "name": "20. 심판", "eng": "Judgement", "keyword": "부활과 재기",
        "event": "과거에 포기했던 일이나 인연이 다시 살아나 극적인 역전승과 명예 회복을 이루는 일",
        "advice": "기적 같은 두 번째 기회가 찾아오는 해이니, 소식이 들려오면 주저 없이 손을 잡으세요."
    },
    21: {
        "roman": "XXI", "symbol": "❖", "color": "#065F46",
        "name": "21. 세계", "eng": "The World", "keyword": "완성과 해피엔딩",
        "event": "오랫동안 공들여 온 목표가 마침내 완벽한 결실을 맺고 더 넓은 세상으로 무대를 넓히는 일",
        "advice": "하나의 큰 주기가 성공적으로 완성됩니다. 해외운이나 이동수도 매우 좋으니 시야를 넓히세요."
    }
}

# 2. 자리별 문장 템플릿
POSITION_TEMPLATES = [
    {
        "title": "첫 번째 변곡점 (초기 운세 흐름)",
        "template": (
            "▶ {year}년 ({age}세) : [{name} ({eng})]\n"
            "{year}년({age}세)에는 생년월일의 초기 파동과 [{name}] 카드가 만나 "
            "'{keyword}'의 기운이 본격적으로 열립니다. 이 해에는 {event}이 찾아올 것입니다. "
            "{advice}\n"
        )
    },
    {
        "title": "두 번째 도약기 (중기 운세 확장)",
        "template": (
            "▶ {year}년 ({age}세) : [{name} ({eng})]\n"
            "{year}년({age}세)에 접어들면 삶의 흐름이 한 단계 확장되며 [{name}] 카드가 상징하는 "
            "'{keyword}'의 운기가 절정에 달합니다. 특히 이 시기에는 {event}을 경험하게 됩니다. "
            "{advice}\n"
        )
    },
    {
        "title": "세 번째 결실기 (장기 운세 완성)",
        "template": (
            "▶ {year}년 ({age}세) : [{name} ({eng})]\n"
            "{year}년({age}세)은 앞선 운의 흐름이 하나로 모이는 중요한 해로, [{name}] 카드의 "
            "'{keyword}' 에너지가 당신의 사주 흐름을 주도합니다. 결과적으로 {event}이 일어나며 큰 전환점을 맞이합니다. "
            "{advice}\n"
        )
    }
]

loaded_images = [None, None, None]


def draw_regular_polygon(canvas, cx, cy, radius, sides, start_angle_deg=0, **kwargs):
    """원의 중심(cx, cy)을 기준으로 정확히 내접하는 다각형을 그리는 보조 함수"""
    points = []
    for i in range(sides):
        angle_rad = math.radians(start_angle_deg + (360 / sides) * i)
        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
        points.extend([x, y])
    return canvas.create_polygon(points, **kwargs)


def draw_centered_magic_seal(canvas, cx, cy, outer_r, symbol_text=None, accent_fill="#18122B"):
    """
    원의 중심(cx, cy)에 오차 없이 정확히 맞물리는 타로 마법진 문양을 그리는 함수
    (바깥 원 + 안쪽 원 + 내접 육망성 + 중앙 코어 원 + 심볼)
    """
    inner_r = outer_r - 6
    core_r = outer_r - 24

    # 1. 바깥 원 & 안쪽 원 (정확히 cx, cy 기준)
    canvas.create_oval(cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r,
                       fill="#18122B", outline="#D4AF37", width=2)
    canvas.create_oval(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
                       fill="", outline="#8A6D1B", width=1)

    # 2. 원 내부에 정확히 내접하는 황금 육망성 (정삼각형 2개 교차)
    draw_regular_polygon(canvas, cx, cy, inner_r, 3, start_angle_deg=-90,
                         fill="", outline="#D4AF37", width=1)
    draw_regular_polygon(canvas, cx, cy, inner_r, 3, start_angle_deg=90,
                         fill="", outline="#D4AF37", width=1)

    # 3. 8방위 눈금 점 (원 테두리 사이에 정확히 배치)
    mid_r = (outer_r + inner_r) / 2
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        px = cx + mid_r * math.cos(rad)
        py = cy + mid_r * math.sin(rad)
        canvas.create_oval(px - 1.5, py - 1.5, px + 1.5, py + 1.5, fill="#F5E8C7", outline="")

    # 4. 중앙 코어 원 (육망성 한가운데)
    canvas.create_oval(cx - core_r, cy - core_r, cx + core_r, cy + core_r,
                       fill=accent_fill, outline="#D4AF37", width=2)

    # 5. 중앙 기하학 심볼 (단일 코드포인트 기호만 사용해 좌우 밀림 완벽 방지)
    if symbol_text:
        canvas.create_text(cx, cy, text=symbol_text,
                           font=("Times New Roman", 24, "bold"),
                           fill="#F5E8C7", anchor="center")


def draw_card_back(canvas, slot_num):
    """뽑기 전 타로 카드 뒷면 디자인을 시각적으로 그리는 함수"""
    canvas.delete("all")
    # 바깥 테두리 및 카드 배경
    canvas.create_rectangle(8, 8, 202, 292, fill="#241734", outline="#D4AF37", width=3)
    canvas.create_rectangle(16, 16, 194, 284, fill="#2E1C44", outline="#9A7B2C", width=1)

    # 사선 격자 무늬 (내부 테두리 16~194, 26~274 영역 안에만 깔끔하게 정렬)
    for y_pos in range(28, 260, 28):
        canvas.create_line(18, y_pos, 192, y_pos + 18, fill="#3D265A", width=1)
        canvas.create_line(18, y_pos + 18, 192, y_pos, fill="#3D265A", width=1)

    # 중앙 마법진 문양 (중심 좌표 105, 148에 정확히 정렬)
    draw_centered_magic_seal(canvas, cx=105, cy=148, outer_r=48, symbol_text="✦", accent_fill="#241734")

    canvas.create_text(105, 52, text=f"✦ CARD {slot_num} ✦", font=("맑은 고딕", 10, "bold"), fill="#D4AF37")
    canvas.create_text(105, 245, text="[ 대기 중 ]", font=("맑은 고딕", 10), fill="#B2A4FF")


def draw_card_front(canvas, idx, card_num, target_year, target_age):
    """뽑힌 타로 카드의 앞면을 이미지 파일 또는 그래픽으로 그리는 함수"""
    canvas.delete("all")
    c_info = TAROT_CARDS[card_num]

    # 1. 상단 연도/나이 배너
    canvas.create_rectangle(8, 8, 202, 40, fill="#D4AF37", outline="#D4AF37")
    canvas.create_text(
        105, 24,
        text=f"{target_year}년 ({target_age}세)",
        font=("맑은 고딕", 11, "bold"), fill="#18122B"
    )

    # 2. 폴더에 이미지 파일(예: 1.png 또는 cards/1.png)이 있는지 확인
    possible_paths = [f"{card_num}.png", f"cards/{card_num}.png", f"{card_num}.gif", f"cards/{card_num}.gif"]
    img_path = next((p for p in possible_paths if os.path.exists(p)), None)

    if img_path:
        try:
            img = tk.PhotoImage(file=img_path)
            loaded_images[idx] = img
            canvas.create_rectangle(8, 40, 202, 292, fill="#18122B", outline="#D4AF37", width=3)
            canvas.create_image(105, 140, image=img)
            canvas.create_rectangle(12, 225, 198, 288, fill="#18122B", outline="#D4AF37", width=1)
            canvas.create_text(105, 245, text=c_info["name"], font=("맑은 고딕", 10, "bold"), fill="#FFFFFF")
            canvas.create_text(105, 270, text=c_info["keyword"], font=("맑은 고딕", 9), fill="#F5E8C7")
            return
        except Exception:
            pass

    # 3. [사진이 없을 때] Canvas 그래픽으로 타로 카드 앞면 직접 그리기
    canvas.create_rectangle(8, 40, 202, 292, fill=c_info["color"], outline="#D4AF37", width=3)
    canvas.create_rectangle(15, 47, 195, 285, outline="#E5C158", width=1)

    # 상단 로마 숫자 표기
    canvas.create_text(105, 65, text=f"― {c_info['roman']} ―", font=("Times New Roman", 13, "bold"), fill="#F5E8C7")

    # 네 모서리 별 장식
    for x, y in [(27, 62), (183, 62), (27, 212), (183, 212)]:
        canvas.create_text(x, y, text="✦", font=("Times New Roman", 10), fill="#D4AF37")

    # 중앙 원형 마법진 + 카드 상징 문양 (원의 중심 105, 140에 100% 일치하도록 제도)
    draw_centered_magic_seal(
        canvas,
        cx=105, cy=140, outer_r=52,
        symbol_text=c_info["symbol"],
        accent_fill=c_info["color"]
    )

    # 하단 카드 이름 & 키워드 명패
    canvas.create_rectangle(15, 225, 195, 285, fill="#120D20", outline="#D4AF37", width=1)
    canvas.create_text(105, 242, text=c_info["name"], font=("맑은 고딕", 11, "bold"), fill="#FFFFFF")
    canvas.create_text(105, 259, text=c_info["eng"], font=("맑은 고딕", 8), fill="#B2A4FF")
    canvas.create_text(105, 275, text=f"« {c_info['keyword']} »", font=("맑은 고딕", 9, "bold"), fill="#F5E8C7")


def draw_tarot_and_predict():
    """버튼 클릭 시 random 함수로 카드를 뽑고 시각적 카드 + 완결된 문장을 출력하는 함수"""
    try:
        b_year = int(entry_year.get().strip())
        b_month = int(entry_month.get().strip())
        b_day = int(entry_day.get().strip())

        birth_date = datetime(b_year, b_month, b_day)
        current_year = datetime.now().year
        if b_year < 1900 or b_year > current_year:
            raise ValueError("연도 범위 오류")
    except ValueError:
        messagebox.showerror("입력 오류", "생년월일의 빈칸(년, 월, 일)을 올바른 숫자로 모두 입력해 주세요!\n(예: 2010년 5월 15일)")
        return

    # 1. random 함수로 21장 중 중복 없이 3장 뽑기
    picked_nums = random.sample(list(TAROT_CARDS.keys()), 3)

    # 2. 생년월일 + 나이 + 뽑힌 카드 번호로 미래 연도 계산
    current_age = current_year - b_year + 1

    offset_1 = ((b_month + current_age + picked_nums[0]) % 3) + 1
    year_1 = current_year + offset_1

    offset_2 = offset_1 + ((b_day + current_age + picked_nums[1]) % 3) + 2
    year_2 = current_year + offset_2

    offset_3 = offset_2 + (((b_year % 100) + current_age + picked_nums[2]) % 3) + 3
    year_3 = current_year + offset_3

    target_years = [year_1, year_2, year_3]
    target_ages = [y - b_year + 1 for y in target_years]

    # 3. 3개의 카드 캔버스에 시각적 카드 앞면 그리기
    for i in range(3):
        draw_card_front(card_canvases[i], i, picked_nums[i], target_years[i], target_ages[i])

    # 4. 하단 텍스트 창에 완결된 문장 출력
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    header = f"📜 [{b_year}년 {b_month}월 {b_day}일생 (현재 {current_age}세) 타로 사주 리딩 결과]\n"
    header += "=" * 72 + "\n\n"
    result_text.insert(tk.END, header)

    for i in range(3):
        c_info = TAROT_CARDS[picked_nums[i]]
        pos_info = POSITION_TEMPLATES[i]

        sentence = pos_info["template"].format(
            year=target_years[i],
            age=target_ages[i],
            name=c_info["name"],
            eng=c_info["eng"],
            keyword=c_info["keyword"],
            event=c_info["event"],
            advice=c_info["advice"]
        )
        result_text.insert(tk.END, f"■ {i+1}. {pos_info['title']}\n")
        result_text.insert(tk.END, sentence + "\n")

    c1, c2, c3 = [TAROT_CARDS[n] for n in picked_nums]
    summary = (
        "=" * 72 + "\n"
        f"💡 [종합 운세 흐름 요약]\n"
        f"당신은 {target_years[0]}년({target_ages[0]}세)에 '{c1['keyword']}'의 기운으로 첫 변화를 맞이한 뒤, "
        f"{target_years[1]}년({target_ages[1]}세)에는 '{c2['keyword']}'의 과정을 거쳐 크게 성장하며, "
        f"마침내 {target_years[2]}년({target_ages[2]}세)에 이르러 '{c3['keyword']}'의 결실을 맺는 사주 흐름을 가지고 있습니다."
    )
    result_text.insert(tk.END, summary)
    result_text.config(state=tk.DISABLED)


# ----------------- Window 창(GUI) 화면 구성 -----------------
window = tk.Tk()
window.title("🔮 타로 × 사주 : 연도별 미래 예언 프로그램")
window.geometry("800x840")
window.configure(bg="#18122B")

# 1. 상단 타이틀
tk.Label(
    window,
    text="🔮 타로 21장 × 사주 : 나의 연도별 미래 점괘",
    font=("맑은 고딕", 18, "bold"),
    bg="#18122B", fg="#F5E8C7", pady=12
).pack()

# 2. 생년월일 입력 영역 (초기값: 2010년 [빈칸]월 [빈칸]일)
input_frame = tk.Frame(window, bg="#18122B")
input_frame.pack(pady=4)

tk.Label(input_frame, text="생년월일 입력 :", font=("맑은 고딕", 11, "bold"), bg="#18122B", fg="#ffffff").grid(row=0, column=0, padx=5)

entry_year = tk.Entry(input_frame, width=7, font=("맑은 고딕", 11), justify="center")
entry_year.insert(0, "2010")  # 처음에 2010년으로 세팅
entry_year.grid(row=0, column=1)
tk.Label(input_frame, text="년", font=("맑은 고딕", 11), bg="#18122B", fg="#ffffff").grid(row=0, column=2, padx=(2, 10))

entry_month = tk.Entry(input_frame, width=4, font=("맑은 고딕", 11), justify="center")
# 월은 비워둠 (__월)
entry_month.grid(row=0, column=3)
tk.Label(input_frame, text="월", font=("맑은 고딕", 11), bg="#18122B", fg="#ffffff").grid(row=0, column=4, padx=(2, 10))

entry_day = tk.Entry(input_frame, width=4, font=("맑은 고딕", 11), justify="center")
# 일도 비워둠 (__일)
entry_day.grid(row=0, column=5)
tk.Label(input_frame, text="일", font=("맑은 고딕", 11), bg="#18122B", fg="#ffffff").grid(row=0, column=6, padx=(2, 10))

# 3. 타로 뽑기 버튼
btn_draw = tk.Button(
    window,
    text="🎴 랜덤으로 타로 카드 3장 뽑기 & 카드 오픈",
    font=("맑은 고딕", 12, "bold"),
    bg="#D4AF37", fg="#18122B",
    activebackground="#B5902B", activeforeground="#18122B",
    relief="raised", padx=18, pady=6, cursor="hand2",
    command=draw_tarot_and_predict
)
btn_draw.pack(pady=12)

# 4. 시각적 타로 카드 3장을 그리는 Canvas 영역
cards_frame = tk.Frame(window, bg="#18122B")
cards_frame.pack(pady=5)

card_canvases = []
for i in range(3):
    cv = tk.Canvas(cards_frame, width=210, height=300, bg="#18122B", highlightthickness=0)
    cv.pack(side="left", padx=12)
    draw_card_back(cv, i + 1)
    card_canvases.append(cv)

# 5. 완결된 문장 출력 영역
result_text = scrolledtext.ScrolledText(
    window,
    width=86, height=15,
    font=("맑은 고딕", 10),
    bg="#221B38", fg="#F5E8C7",
    padx=15, pady=15,
    wrap=tk.WORD
)
result_text.pack(pady=12, padx=25)
result_text.insert(tk.END, "위에서 생년월일(2010년 __월 __일)을 입력하고 [타로 카드 3장 뽑기 & 카드 오픈] 버튼을 눌러주세요.")
result_text.config(state=tk.DISABLED)

# 실행 시 바로 '월' 입력칸에 커서가 가도록 설정
entry_month.focus_set()

window.mainloop()
