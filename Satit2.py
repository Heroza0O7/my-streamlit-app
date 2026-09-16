import streamlit as st

# =========================================================================
# ตั้งค่าหน้าเว็บและธีม (Modern Scientific / Clean Theme)
# =========================================================================
st.set_page_config(page_title="เครื่องคำนวณผสมสารละลาย", layout="centered")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'IBM Plex Sans Thai', sans-serif;
        }
        html, body {
            background-color: #eef2f1 !important;
        }
        .stApp {
            background-color: #eef2f1;
            background-image:
                linear-gradient(#e2e8e6 1px, transparent 1px),
                linear-gradient(90deg, #e2e8e6 1px, transparent 1px);
            background-size: 28px 28px;
        }
        /* บังคับสีตัวอักษรของหัวข้อ, ป้ายกำกับ, และข้อความทั่วไปให้เข้มเสมอ
           กันปัญหาตัวอักษรกลืนกับพื้นหลังไม่ว่าธีมของเบราว์เซอร์/ระบบจะเป็นอย่างไร */
        h1, h2, h3, p, label, .stMarkdown, .stCaption, span {
            color: #16232a !important;
        }
        [data-testid="stCaptionContainer"] {
            color: #52646c !important;
        }

        /* บังคับสไตล์ของ widget ภายใน Streamlit (ช่องกรอกตัวเลข, dropdown, ปุ่ม)
           ให้เป็นธีมสว่างเสมอ โดยไม่ต้องพึ่งไฟล์ .streamlit/config.toml */
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        input[type="number"],
        input[type="text"],
        textarea {
            background-color: #ffffff !important;
            color: #16232a !important;
            border: 1px solid #d9e1de !important;
        }
        div[data-baseweb="select"] *,
        div[data-baseweb="popover"] * {
            color: #16232a !important;
        }
        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }
        button {
            background-color: #ffffff !important;
            color: #16232a !important;
            border: 1px solid #0e7c86 !important;
        }
        button p, button span {
            color: #16232a !important;
        }
        button[kind="primary"], button[data-testid="baseButton-primary"] {
            background-color: #0e7c86 !important;
            border-color: #0e7c86 !important;
        }
        button[kind="primary"] p, button[data-testid="baseButton-primary"] p,
        button[kind="primary"] span, button[data-testid="baseButton-primary"] span {
            color: #ffffff !important;
        }

        .readout {
            background: #0f2226;
            border: 1px solid #1c3d42;
            border-radius: 6px;
            padding: 24px;
            text-align: center;
        }
        .readout-num {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 2.2rem;
            color: #7fe3c9 !important;
            font-weight: 600;
        }
        .readout-unit {
            font-family: 'IBM Plex Mono', monospace;
            color: #4f9a8f !important;
            font-size: 1rem;
        }
        .readout-caption {
            color: #a8c7c2 !important;
            font-size: 0.85rem;
            margin-top: 4px;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'IBM Plex Mono', monospace;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("เครื่องคำนวณผสมสารละลาย")
st.markdown("**C₁V₁ + C₂V₂ + ... + CₙVₙ = C<sub>รวม</sub> · V<sub>รวม</sub>**", unsafe_allow_html=True)
st.divider()

# =========================================================================
# เก็บสถานะรายการสารละลาย (Dynamic N สาร) ไว้ใน session_state
# =========================================================================
if "substances" not in st.session_state:
    st.session_state.substances = [{"c": 0.0, "v": 0.0}]

mode_labels = {
    "c_total": "หาความเข้มข้นรวม (C รวม)",
    "v_total": "หาปริมาตรรวม / ปริมาตรตัวทำละลายที่ต้องเติม",
    "find_vi": "หาปริมาตรของสารที่ไม่ทราบ (Vi)",
    "find_ci": "หาความเข้มข้นของสารที่ไม่ทราบ (Ci)",
}
mode = st.selectbox("โหมดคำนวณ", options=list(mode_labels.keys()), format_func=lambda k: mode_labels[k])

substances_caption = "สารละลายที่ทราบค่า" if mode in ("c_total", "v_total") else "สารละลายอื่นที่ทราบค่าครบ"
st.subheader(substances_caption)

# หัวตาราง
head_c, head_v, head_btn = st.columns([3, 3, 1])
head_c.caption("C (mol/L)")
head_v.caption("V (mL)")
head_btn.caption(" ")

# วนแสดงแต่ละแถวของสาร พร้อมปุ่มลบรายตัว
for i, item in enumerate(st.session_state.substances):
    col_c, col_v, col_btn = st.columns([3, 3, 1])
    item["c"] = col_c.number_input(
        f"C{i + 1}", min_value=0.0, value=item["c"], step=0.1, key=f"c_{i}", label_visibility="collapsed"
    )
    item["v"] = col_v.number_input(
        f"V{i + 1}", min_value=0.0, value=item["v"], step=0.1, key=f"v_{i}", label_visibility="collapsed"
    )
    if col_btn.button("✕", key=f"remove_{i}", help="ลบสารนี้"):
        st.session_state.substances.pop(i)
        st.rerun()

if st.button("+ เพิ่มสาร"):
    st.session_state.substances.append({"c": 0.0, "v": 0.0})
    st.rerun()

st.divider()

# =========================================================================
# ช่องกรอกเพิ่มเติมตามโหมดที่เลือก
# =========================================================================
unknown_c = None
unknown_v = None
target_c = None
target_v = None

if mode == "v_total":
    target_c = st.number_input("C รวมเป้าหมาย (mol/L)", min_value=0.0, value=0.0, step=0.1)

elif mode == "find_vi":
    unknown_c = st.number_input("C ของสารที่ไม่ทราบปริมาตร (mol/L)", min_value=0.0, value=0.0, step=0.1)
    col1, col2 = st.columns(2)
    target_c = col1.number_input("C รวมเป้าหมาย (mol/L)", min_value=0.0, value=0.0, step=0.1)
    target_v = col2.number_input("V รวมเป้าหมาย (mL)", min_value=0.0, value=0.0, step=0.1)

elif mode == "find_ci":
    unknown_v = st.number_input("V ของสารที่ไม่ทราบความเข้มข้น (mL)", min_value=0.0, value=0.0, step=0.1)
    col1, col2 = st.columns(2)
    target_c = col1.number_input("C รวมเป้าหมาย (mol/L)", min_value=0.0, value=0.0, step=0.1)
    target_v = col2.number_input("V รวมเป้าหมาย (mL)", min_value=0.0, value=0.0, step=0.1)

st.write("")
calculate = st.button("คำนวณ", type="primary", use_container_width=True)

# =========================================================================
# Logic การคำนวณ (เหมือนเวอร์ชัน Flask ทุกประการ)
# =========================================================================
if calculate:
    substances = [(item["c"], item["v"]) for item in st.session_state.substances]
    sum_cv = sum(c * v for c, v in substances)
    sum_v = sum(v for c, v in substances)

    try:
        if mode == "c_total":
            if sum_v == 0:
                raise ValueError("ปริมาตรรวมเป็น 0 หารไม่ได้")
            c_total = sum_cv / sum_v
            st.markdown(
                f"""<div class="readout">
                        <div class="readout-num">{c_total:.6f} <span class="readout-unit">mol/L</span></div>
                        <div class="readout-caption">ความเข้มข้นรวม (C รวม)</div>
                    </div>""",
                unsafe_allow_html=True,
            )

        elif mode == "v_total":
            if target_c == 0:
                raise ValueError("C รวมเป้าหมายเป็น 0 หารไม่ได้")
            v_total = sum_cv / target_c
            v_add = v_total - sum_v
            if v_add < 0:
                raise ValueError("C เป้าหมายสูงเกินกว่าที่เป็นไปได้จากสารที่มีอยู่")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(
                    f"""<div class="readout">
                            <div class="readout-num">{v_total:.6f}<span class="readout-unit"> mL</span></div>
                            <div class="readout-caption">ปริมาตรรวม (V รวม)</div>
                        </div>""",
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    f"""<div class="readout">
                            <div class="readout-num">{v_add:.6f}<span class="readout-unit"> mL</span></div>
                            <div class="readout-caption">ตัวทำละลายที่ต้องเติมเพิ่ม</div>
                        </div>""",
                    unsafe_allow_html=True,
                )

        elif mode == "find_vi":
            if unknown_c == 0:
                raise ValueError("Ci เป็น 0 หารไม่ได้")
            vi = (target_c * target_v - sum_cv) / unknown_c
            if vi < 0:
                raise ValueError("ค่าที่คำนวณได้ติดลบ ข้อมูลที่ป้อนไม่สอดคล้องกัน")
            st.markdown(
                f"""<div class="readout">
                        <div class="readout-num">{vi:.6f} <span class="readout-unit">mL</span></div>
                        <div class="readout-caption">ปริมาตร (Vi) ที่ต้องใช้</div>
                    </div>""",
                unsafe_allow_html=True,
            )

        elif mode == "find_ci":
            if unknown_v == 0:
                raise ValueError("Vi เป็น 0 หารไม่ได้")
            ci = (target_c * target_v - sum_cv) / unknown_v
            if ci < 0:
                raise ValueError("ค่าที่คำนวณได้ติดลบ ข้อมูลที่ป้อนไม่สอดคล้องกัน")
            st.markdown(
                f"""<div class="readout">
                        <div class="readout-num">{ci:.6f} <span class="readout-unit">mol/L</span></div>
                        <div class="readout-caption">ความเข้มข้น (Ci) ที่ต้องใช้</div>
                    </div>""",
                unsafe_allow_html=True,
            )

    except ValueError as err:
        st.error(str(err))