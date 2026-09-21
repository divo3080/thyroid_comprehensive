import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Hệ Thống Chẩn Đoán, Điều Trị Cá Thể Hóa & Phân Tích Case Lâm Sàng Bệnh Lý Tuyến Giáp",
    page_icon="🩺",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .section-box {
        background-color: #F8FAFC;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
        margin-bottom: 1rem;
    }
    .alert-box {
        background-color: #FEF2F2;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #EF4444;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #F0FDF4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #22C55E;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🩺 HỆ THỐNG TRỢ LÝ LÂM SÀNG: CHẨN ĐOÁN, ĐIỀU TRỊ CÁ THỂ HÓA & PHÂN TÍCH CASE LÂM SÀNG BỆNH LÝ TUYẾN GIÁP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tích hợp dữ liệu Lâm Sàng, Cận Lâm Sàng, Hình Ảnh Học, Yếu Tố Nguy Cơ, Thang Điểm BWPS, Tiên Lượng & Phân Tích Cơ Chế Sinh Lý Bệnh - Dược Lý Thuốc</div>', unsafe_allow_html=True)

st.divider()

# ==========================================
# SIDEBAR: THÔNG TIN HÀNH CHÍNH & NGUY CƠ
# ==========================================
st.sidebar.header("👤 THÔNG TIN BỆNH NHÂN & BỆNH NỀN")

patient_name = st.sidebar.text_input("Họ và tên bệnh nhân", value="Nguyễn Văn A")
age = st.sidebar.number_input("Tuổi", min_value=1, max_value=120, value=38)
gender = st.sidebar.selectbox("Giới tính", ["Nữ", "Nam"])
weight_kg = st.sidebar.number_input("Cân nặng (kg)", min_value=1.0, max_value=200.0, value=58.0, step=0.5)

is_pregnant = False
preg_trimester = "Không"
if gender == "Nữ":
    is_pregnant = st.sidebar.checkbox("Đang mang thai")
    if is_pregnant:
        preg_trimester = st.sidebar.radio("Giai đoạn thai kỳ", ["3 tháng đầu (Quý 1)", "3 tháng giữa / cuối (Quý 2-3)"])

comorbidities = st.sidebar.multiselect(
    "Yếu tố nguy cơ & Bệnh lý nền",
    [
        "Người cao tuổi (> 60 tuổi)",
        "Bệnh động mạch vành / Thiếu máu cơ tim",
        "Suy tim sung huyết",
        "Rung nhĩ / Rối loạn nhịp",
        "Hen phế quản / COPD",
        "Bệnh gan / Men gan tăng cao (> 3xULN)",
        "Tiền sử dị ứng Methimazole hoặc PTU",
        "Tiền sử bệnh tự miễn khác (ĐTĐ typ 1, Bạch biến, Viêm khớp dạng thấp)",
        "Hút thuốc lá (Nguy cơ bệnh mắt Basedow nặng)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Ghi chú:** Ứng dụng hỗ trợ ra quyết định lâm sàng chuyên sâu cho bác sĩ. Mọi thông tin cần đối chiếu toàn diện với tình trạng lâm sàng thực tế.")

# ==========================================
# TABS HỆ THỐNG
# ==========================================
tab_input, tab_bwps, tab_diag_diff, tab_treatment, tab_case_study = st.tabs([
    "📋 1. Dữ Liệu Lâm Sàng & Cận Lâm Sàng",
    "📊 2. Đánh Giá Mức Độ (BWPS)",
    "🔍 3. Chẩn Đoán Phân Biệt & Tiên Lượng",
    "💊 4. Phác Đồ Điều Trị Cá Thể Hóa",
    "🧬 5. Phân Tích Case Lâm Sàng & Sinh Lý Bệnh"
])

# ==========================================
# TAB 1: NHẬP DỮ LIỆU
# ==========================================
with tab_input:
    col_cl, col_paracl = st.columns(2)
    
    with col_cl:
        st.subheader("🫀 1. Triệu Chứng Lâm Sàng & Thám Khám")
        
        st.markdown("##### A. Dấu hiệu sinh tồn & Chuyển hóa toàn thân:")
        hr = st.number_input("Nhịp tim lúc nghỉ (lần/phút)", min_value=30, max_value=220, value=115)
        temp = st.number_input("Thân nhiệt (°C)", min_value=35.0, max_value=43.0, value=37.5, step=0.1)
        weight_change = st.number_input("Thay đổi cân nặng (kg trong 1-2 tháng qua) [Dương: tăng cân, Âm: sụt cân]", min_value=-30.0, max_value=30.0, value=-5.0, step=0.5)
        
        st.markdown("##### B. Hệ Tiêu hóa & Thần kinh trung ương:")
        stool_freq = st.selectbox(
            "Tính chất đi tiêu & Tiêu hóa",
            ["Bình thường", "Tăng nhu động / Tiêu phân lỏng 3-5 lần/ngày", "Tiêu chảy rầm rộ / Đau bụng / Nôn ói", "Vàng da chưa rõ nguyên nhân", "Táo bón dai dẳng kéo dài"]
        )
        cns_status = st.selectbox(
            "Trạng thái Thần kinh - Tâm thần",
            ["Bình thường / Lo âu nhẹ", "Kích động, bồn chồn, run tay rõ", "Lú lẫn, sảng, mê sảng, psychosis", "Co giật, hôn mê"]
        )
        
        st.markdown("##### C. Triệu chứng gợi ý Suy giáp:")
        hypo_symptoms = st.multiselect(
            "Các triệu chứng giảm chuyển hóa",
            ["Sợ lạnh, da khô, niêm mạc khô", "Mệt mỏi, chậm chạp, giảm trí nhớ", "Tăng cân dù ăn uống bình thường", "Táo bón dai dẳng", "Phù niêm toàn thân, mặt tròn", "Khàn tiếng, lưỡi to", "Rong kinh / Rối loạn kinh nguyệt"]
        )
        
        st.markdown("##### D. Khám tại chỗ Tuyến giáp, Mắt & Da:")
        goiter_exam = st.selectbox(
            "Khám tuyến giáp (Lâm sàng)",
            [
                "Không bướu / Tuyến giáp to nhẹ độ IA/IB",
                "Bướu giáp lan tỏa, mật độ mềm, có tiếng thổi tâm thu/liên tục (Bướu mạch)",
                "Bướu nhân đơn độc hoặc Đa nhân giáp",
                "Tuyến giáp to gây chèn ép (khó thở, khó nuốt, khàn tiếng)",
                "Tuyến giáp to nhẹ, đau nhiều khi sờ, lan lên tai/góc hàm"
            ]
        )
        eye_exam = st.multiselect(
            "Biểu hiện mắt (Basedow Orbitopathy)",
            [
                "Co cơ mi trên / Hở khe mi (Dalrymple, von Graefe)",
                "Phù mi mắt / Kết mạc",
                "Lồi mắt thực sự (> 3mm so với bình thường)",
                "Tổn thương cơ vận nhãn (nhìn đôi/song thị)",
                "Tổn thương giác mạc (viêm/loét giác mạc)",
                "Giảm thị lực / Mất thị lực do chèn ép thần kinh thị"
            ]
        )
        pretibial_edema = st.checkbox("Phù niêm khu trú trước xương chày (Thâm nhiễm GAGs)")

    with col_paracl:
        st.subheader("🧪 2. Cận Lâm Sàng & Hình Ảnh Học")
        
        st.markdown("##### A. Bilan Chức năng Giáp & Kháng thể:")
        tsh = st.number_input("TSH (mIU/L) [Tham chiếu: 0.4 - 4.5 mIU/L]", min_value=0.000, max_value=150.0, value=0.005, step=0.01, format="%.3f")
        ft4 = st.number_input("FT4 (ng/dL) [Tham chiếu: 0.9 - 2.0 ng/dL]", min_value=0.00, max_value=20.0, value=3.8, step=0.1)
        ft3 = st.number_input("FT3 (pg/mL) [Tham chiếu: 2.0 - 4.4 pg/mL]", min_value=0.00, max_value=50.0, value=9.2, step=0.1)
        
        trab = st.selectbox("Kháng thể TRAb (TSH Receptor Antibody) [Đặc hiệu Basedow]", ["Chưa làm", "Dương tính (+)", "Âm tính (-)"])
        tpo_ab = st.selectbox("Kháng thể TPO-Ab / Anti-TPO [Đặc hiệu Hashimoto]", ["Chưa làm", "Dương tính (+)", "Âm tính (-)"])
        
        st.markdown("##### B. Hình Ảnh Học (Siêu âm & Xạ hình):")
        us_findings = st.selectbox(
            "Siêu âm Doppler tuyến giáp",
            [
                "Chưa thực hiện",
                "Bướu giáp to lan tỏa, giảm âm, tăng sinh mạch máu rất mạnh ('Thyroid Inferno' / Thảm mạch)",
                "Nhân độc tuyến giáp (Nhân đơn độc, tăng sinh mạch ngoại vi/trung tâm)",
                "Đa nhân giáp hai thùy",
                "Nang giáp / Nhân giáp gợi ý EU-TIRADS 2-3 (Lành tính)",
                "Nhân giáp nghi ngờ cao EU-TIRADS 4-5 (Bờ không đều, vi vôi hóa, chiều cao > chiều rộng)",
                "Tuyến giáp giảm âm không đều, dải xơ giả nhân (Gợi ý Hashimoto)",
                "Tuyến giáp giảm âm không đều dạng ổ, giảm tưới máu (Gợi ý Viêm giáp bán cấp)"
            ]
        )
        scan_findings = st.selectbox(
            "Xạ hình tuyến giáp (131-I hoặc 99m-Tc)",
            [
                "Chưa thực hiện",
                "Tăng bắt xạ lan tỏa đều hai thùy, có hình ảnh 'Góc thoát' ở giờ thứ 2-6",
                "Tăng bắt xạ tập trung tại nhân độc (Nhân nóng), mô giáp xung quanh bị ức chế",
                "Bắt xạ không đều kiểu 'khảm' (Đa nhân độc)",
                "Giảm bắt xạ nặng hoặc Không bắt xạ (Độ tập trung < 1-2%) [Viêm giáp / Quá tải Iod]"
            ]
        )
        
        st.markdown("##### C. Xét nghiệm An toàn, Biến chứng & Chỉ số Viêm:")
        anc = st.number_input("Bạch cầu Neutrophil (ANC) (/mm³) [An toàn > 1500]", min_value=0, max_value=30000, value=4500)
        alt = st.number_input("Men gan ALT / AST (U/L) [Bình thường < 40]", min_value=0, max_value=2000, value=32)
        crp_esr = st.selectbox("Chỉ số viêm CRP / Vận tốc máu lắng (ESR)", ["Bình thường", "Tăng cao rõ rệt (CRP > 20 mg/L hoặc ESR > 50 mm/h)"])
        cholesterol = st.number_input("Cholesterol toàn phần (mg/dL) [Tăng trong suy giáp]", min_value=0, max_value=600, value=185)

# ==========================================
# TAB 2: ĐÁNH GIÁ MỨC ĐỘ NẶNG & BWPS
# ==========================================
with tab_bwps:
    st.subheader("📊 Bảng Tính Điểm Burch - Wartofsky Point Scale (BWPS) & Đánh Giá Mức Độ Nặng")
    st.caption("Thang điểm BWPS giúp phát hiện khẩn cấp Dọa Bão Giáp (Impending Storm) và Bão Giáp (Thyroid Storm).")
    
    # BWPS Calculations
    t_score = 0
    if temp < 37.8: t_score = 0
    elif 37.8 <= temp <= 38.2: t_score = 5
    elif 38.3 <= temp <= 38.8: t_score = 10
    elif 38.9 <= temp <= 39.4: t_score = 15
    elif 39.5 <= temp <= 39.9: t_score = 20
    else: t_score = 25
    
    c_score = 0
    if cns_status == "Bình thường / Lo âu nhẹ": c_score = 0
    elif cns_status == "Kích động, bồn chồn, run tay rõ": c_score = 10
    elif cns_status == "Lú lẫn, sảng, mê sảng, psychosis": c_score = 20
    else: c_score = 30
    
    g_score = 0
    if stool_freq in ["Bình thường", "Táo bón dai dẳng kéo dài"]: g_score = 0
    elif stool_freq in ["Tăng nhu động / Tiêu phân lỏng 3-5 lần/ngày", "Tiêu chảy rầm rộ / Đau bụng / Nôn ói"]: g_score = 10
    else: g_score = 20 # Vàng da
    
    h_score = 0
    if hr < 90: h_score = 0
    elif 90 <= hr <= 109: h_score = 5
    elif 110 <= hr <= 119: h_score = 10
    elif 120 <= hr <= 129: h_score = 15
    elif 130 <= hr <= 139: h_score = 20
    else: h_score = 25
    
    st.markdown("##### Các yếu tố tim mạch & Yếu tố thúc đẩy bổ sung:")
    col_chf, col_af, col_precip = st.columns(3)
    
    with col_chf:
        chf_status = st.selectbox("Suy tim sung huyết (CHF)", ["Không có", "Nhẹ (Phù chân)", "Trung bình (Ran ẩm đáy phổi)", "Nặng (Phù phổi cấp)"])
        chf_score = 0 if chf_status == "Không có" else (5 if chf_status == "Nhẹ (Phù chân)" else (10 if chf_status == "Trung bình (Ran ẩm đáy phổi)" else 15))
        
    with col_af:
        af_status = st.checkbox("Có Rung nhĩ (Atrial Fibrillation)")
        af_score = 10 if af_status else 0
        
    with col_precip:
        precip_status = st.checkbox("Có Yếu tố thúc đẩy (Nhiễm trùng, phẫu thuật, chấn thương, ngưng KGTH đột ngột, Iod/131-I)")
        precip_score = 10 if precip_status else 0
        
    bwps_total = t_score + c_score + g_score + h_score + chf_score + af_score + precip_score
    
    st.metric("TỔNG ĐIỂM BURCH - WARTOFSKY (BWPS)", f"{bwps_total} ĐIỂM")
    
    if bwps_total >= 45:
        st.error("🚨 **CHẨN ĐOÁN: CƠN BÃO GIÁP (THYROID STORM) - MỨC ĐỘ CỰC KỲ NẶNG**\n\n-> Chỉ định chuyển khoa Hồi sức Tích cực (ICU), thiết lập theo dõi huyết động liên tục và điều trị phối hợp đa mô thức khẩn cấp!")
    elif 25 <= bwps_total <= 44:
        st.warning("⚠️ **CHẨN ĐOÁN: DỌA BÃO GIÁP (IMPENDING THYROID STORM) - MỨC ĐỘ NẶNG**\n\n-> Nguy cơ cao tiến triển thành Bão giáp. Bệnh nhân cần được theo dõi sát tại khoa Nội tiết/Cấp cứu và điều trị tích cực bằng thuốc kháng giáp liều cao & chẹn Beta.")
    else:
        st.success("✅ **KẾT QUẢ: CHƯA CÓ DẤU HIỆU BÃO GIÁP (BWPS < 25 điểm)**")

# ==========================================
# SHARED DIAGNOSTIC & SEVERITY LOGIC
# ==========================================
primary_diag = ""
diag_category = "" # HYPER, HYPO, THYROIDITIS, NORMAL

# Diagnostic Algorithm
if tsh < 0.4:
    if ft4 > 2.0 or ft3 > 4.4:
        if trab == "Dương tính (+)" or "Bướu mạch" in goiter_exam or "Thyroid Inferno" in us_findings or "Tăng bắt xạ lan tỏa" in scan_findings:
            primary_diag = "Bệnh Basedow (Graves' Disease) - Hội chứng Nhiễm độc giáp Cường giáp Tự miễn"
            diag_category = "HYPER"
        elif "Nhân nóng" in scan_findings or "Nhân độc" in us_findings:
            primary_diag = "Bướu nhân độc / Đa nhân độc tuyến giáp (Plummer Disease)"
            diag_category = "HYPER"
        elif "Giảm bắt xạ" in scan_findings or "đau nhiều khi sờ" in goiter_exam or "Tăng cao rõ rệt" in crp_esr:
            primary_diag = "Viêm giáp bán cấp de Quervain (Nhiễm độc giáp do viêm phá hủy nang giáp)"
            diag_category = "THYROIDITIS"
        else:
            primary_diag = "Hội chứng Nhiễm độc giáp chưa phân loại (Cần làm thêm TRAb hoặc Xạ hình)"
            diag_category = "HYPER"
    else:
        primary_diag = "Cường giáp dưới lâm sàng (Subclinical Hyperthyroidism)"
        diag_category = "HYPER"
elif tsh > 4.5:
    if ft4 < 0.9:
        primary_diag = "Suy giáp lâm sàng (Overt Hypothyroidism)"
        diag_category = "HYPO"
        if tpo_ab == "Dương tính (+)" or "dải xơ giả nhân" in us_findings:
            primary_diag += " do Viêm giáp tự miễn Hashimoto"
    else:
        primary_diag = "Suy giáp dưới lâm sàng (Subclinical Hypothyroidism)"
        diag_category = "HYPO"
        if tpo_ab == "Dương tính (+)":
            primary_diag += " do Viêm giáp Hashimoto"
else:
    if ft4 < 0.9:
        primary_diag = "Suy giáp thứ phát / Thứ phát do tuyến yên (Central Hypothyroidism)"
        diag_category = "HYPO"
    else:
        primary_diag = "Chức năng tuyến giáp bình thường (Bình giáp)"
        diag_category = "NORMAL"

# ==========================================
# TAB 3: CHẨN ĐOÁN PHÂN BIỆT & TIÊN LƯỢNG
# ==========================================
with tab_diag_diff:
    st.subheader("🔍 1. Chẩn Đoán Xác Định & Phân Biệt Nguyên Nhân")
    st.markdown(f"#### 📌 Chẩn đoán hướng đến: **{primary_diag}**")
    
    st.markdown("---")
    st.markdown("##### 📊 Ma trận so sánh đặc điểm lâm sàng & cận lâm sàng phân biệt nguyên nhân:")
    
    diff_data = [
        {"Tiêu chí": "Bản chất bệnh", "Bệnh Basedow": "Cường giáp tự miễn (Tăng tổng hợp)", "Bướu nhân độc": "Cường giáp do nhân tự chủ", "Viêm giáp de Quervain": "Viêm phá hủy nang giáp (Thoát hormone)", "Viêm giáp Hashimoto": "Viêm tự miễn gây phá hủy xơ hóa (Suy giáp)"},
        {"Tiêu chí": "Kháng thể TRAb", "Bệnh Basedow": "Dương tính (+) (80-90%)", "Bướu nhân độc": "Âm tính (-)", "Viêm giáp de Quervain": "Âm tính (-)", "Viêm giáp Hashimoto": "Thường âm tính (-)"},
        {"Tiêu chí": "Kháng thể Anti-TPO", "Bệnh Basedow": "Có thể dương tính nhẹ", "Bướu nhân độc": "Âm tính (-)", "Viêm giáp de Quervain": "Âm tính (-)", "Viêm giáp Hashimoto": "Dương tính rất cao (+) (>90%)"},
        {"Tiêu chí": "Xạ hình 131-I", "Bệnh Basedow": "Tăng bắt xạ lan tỏa (Có góc thoát)", "Bướu nhân độc": "Tăng bắt xạ tại nhân nóng", "Viêm giáp de Quervain": "Giảm / Không bắt xạ (< 1-2%)", "Viêm giáp Hashimoto": "Bắt xạ không đều hoặc giảm"},
        {"Tiêu chí": "Siêu âm Doppler", "Bệnh Basedow": "Tăng sinh mạch rất mạnh ('Inferno')", "Bướu nhân độc": "Nhân khu trú tăng tưới máu", "Viêm giáp de Quervain": "Vùng giảm âm, giảm tưới máu", "Viêm giáp Hashimoto": "Giảm âm không đều, dải xơ"},
        {"Tiêu chí": "Biểu hiện mắt/Da", "Bệnh Basedow": "Lồi mắt, Phù niêm trước xương chày", "Bướu nhân độc": "Không có", "Viêm giáp de Quervain": "Không có", "Viêm giáp Hashimoto": "Không có"},
        {"Tiêu chí": "Thuốc KGTH", "Bệnh Basedow": "Chỉ định chính (12-18 tháng)", "Bướu nhân độc": "Chuẩn bị trước 131-I hoặc mổ", "Viêm giáp de Quervain": "❌ CHỐNG CHỈ ĐỊNH (Không dùng)", "Viêm giáp Hashimoto": "❌ Không dùng (Chỉ dùng LT4)"}
    ]
    st.table(pd.DataFrame(diff_data))
    
    st.markdown("---")
    st.subheader("📈 2. Đánh Giá Tiên Lượng & Nguy Cơ Biến Chứng")
    
    if diag_category == "HYPER" and "Basedow" in primary_diag:
        st.markdown("##### 🔮 Tiên lượng Bệnh Basedow:")
        st.markdown("""
        - **Tỷ lệ lui bệnh nội khoa:** Khoảng 40 – 50% sau đợt điều trị 12 – 18 tháng bằng thuốc kháng giáp tổng hợp (KGTH).
        - **Yếu tố tiên lượng TÁI PHÁT cao:**
            - Nồng độ kháng thể $TRAb$ vẫn duy trì dương tính cao sau đợt điều trị.
            - Bướu giáp to dai dẳng hoặc bướu mạch nhiều.
            - Nam giới, tuổi khởi phát trẻ (< 30 tuổi).
            - Bệnh nhân có thói quen **hút thuốc lá** (tăng nguy cơ tái phát & làm nặng tiến triển bệnh mắt).
        - **Tiên lượng Bệnh mắt Basedow:** Cần theo dõi sát mức độ hoạt động của mắt. Nếu có tổn thương giác mạc hoặc chèn ép thần kinh thị, tiên lượng thị lực nguy hiểm nếu không dùng Corticoid liều cao hoặc phẫu thuật giải áp hốc mắt.
        """)
    elif diag_category == "THYROIDITIS":
        st.markdown("##### 🔮 Tiên lượng Viêm giáp bán cấp de Quervain:")
        st.markdown("""
        - **Diễn tiến tự nhiên:** Thường diễn tiến qua 4 giai đoạn: *Nhiễm độc giáp (2-6 tuần) -> Bình giáp thoáng qua -> Suy giáp thoáng qua (2-8 tuần) -> Hồi phục hoàn toàn (bình giáp)*.
        - **Tiên lượng lâu dài:** Đa số hồi phục hoàn toàn chức năng giáp sau 3 - 6 tháng. Chỉ khoảng < 5% tiến triển thành suy giáp vĩnh viễn cần điều trị Levothyroxine lâu dài.
        """)
    elif diag_category == "HYPO":
        st.markdown("##### 🔮 Tiên lượng Suy giáp & Viêm giáp Hashimoto:")
        st.markdown("""
        - **Tiên lượng lâu dài:** Suy giáp lâm sàng do Hashimoto là tình trạng **mạn tính vĩnh viễn**, đòi hỏi điều trị thay thế hormone bằng Levothyroxine ($LT_4$) suốt đời.
        - **Tiên lượng phục hồi:** Khi được điều trị đạt mục tiêu $TSH$ bình thường, bệnh nhân có chất lượng cuộc sống và tuổi thọ hoàn toàn bình thường như người không mắc bệnh.
        """)
    else:
        st.markdown("##### 🔮 Tiên lượng Chức năng giáp:")
        st.markdown("- Tiên lượng tốt. Cần kiểm tra định kỳ mỗi 6 - 12 tháng.")

# ==========================================
# TAB 4: PHÁC ĐỒ ĐIỀU TRỊ CÁ THỂ HÓA
# ==========================================
with tab_treatment:
    st.subheader("💊 Phác Đồ Điều Trị Cá Thể Hóa & Liều Thuốc Cụ Thể")
    
    if diag_category == "HYPER" and "Basedow" in primary_diag:
        st.markdown("### 🅰️ PHÁC ĐỒ ĐIỀU TRỊ BỆNH BASEDOW / CƯỜNG GIÁP")
        
        # 1. ATD Selection
        st.markdown("#### 1. Thuốc Kháng Giáp Tổng Hợp (KGTH / Thioamide): Liều Lượng Ban Đầu & Tấn Công")
        if anc < 500:
            st.error("❌ **CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI KGTH:** Bệnh nhân đang bị **Tuyệt lạp bạch cầu hạt (Neutrophil < 500/mm³)**. Ngừng ngay lập tức tất cả các thuốc KGTH! Nhập viện cách ly, dùng kháng sinh phổ rộng & cân nhắc G-CSF.")
        elif "Bệnh gan / Men gan tăng cao (> 3xULN)" in comorbidities or alt > 120:
            st.warning("⚠️ **LƯU Ý ĐỘC TÍNH GAN:** Men gan tăng cao hoặc bệnh gan nền. **CHỐNG CHỈ ĐỊNH PTU** do nguy cơ hoại tử gan tối cấp. Ưu tiên **Methimazole** và theo dõi men gan mỗi 1-2 tuần.")
        else:
            if is_pregnant and preg_trimester == "3 tháng đầu (Quý 1)":
                st.success("👉 **ƯU TIÊN CHỈ ĐỊNH: Propylthiouracil (PTU)**")
                st.markdown("- **Lý do:** PTU gắn kết protein huyết tương mạnh, khó qua nhau thai, tránh nguy cơ dị tật bất sản da đầu (Aplasia cutis) cho thai nhi trong Quý 1.")
                st.markdown("- **Liều tấn công:** PTU **100 - 150 mg x 3 lần/ngày** (Tổng 300 - 450 mg/ngày, uống chia đều mỗi 8 giờ).")
                st.markdown("- **Thời gian tấn công:** **6 - 8 tuần**.")
                st.markdown("- **Lưu ý thai kỳ:** Chuyển sang Methimazole từ Quý 2 trở đi (tuần thứ 13-14) để giảm độc tính gan cho mẹ.")
            elif bwps_total >= 45:
                st.success("👉 **CẤP CỨU CƠN BÃO GIÁP: Propylthiouracil (PTU)**")
                st.markdown("- **Lý do:** PTU có tác dụng kép: vừa khóa tổng hợp hormone mới tại tuyến giáp, vừa **ức chế 5'-deiodinase ngăn chuyển T4 thành T3 ngoại vi**.")
                st.markdown("- **Phác đồ cấp cứu:** PTU **liều tải 600 mg** (uống/bơm xông) -> **liều duy trì 200 mg mỗi 4 - 6 giờ** (Tổng 1200 - 1500 mg/ngày).")
            else:
                st.success("👉 **ƯU TIÊN LỰA CHỌN HÀNG ĐẦU: Methimazole (Thiamazole / Carbimazole)**")
                st.markdown("- **Lý do:** Tác dụng mạnh hơn PTU 10-15 lần, tích lũy kéo dài trong tuyến giáp (> 24h), **uống 1 lần/ngày** nâng cao tuân thủ, ít độc gan nặng hơn PTU.")
                if ft4 > 4.0 or bwps_total >= 25:
                    st.markdown("- **Liều tấn công (6 - 8 tuần):** Methimazole **30 mg/ngày** (uống 1 lần buổi sáng).")
                elif ft4 > 2.0:
                    st.markdown("- **Liều tấn công (6 - 8 tuần):** Methimazole **15 - 20 mg/ngày** (uống 1 lần buổi sáng).")
                else:
                    st.markdown("- **Liều tấn công (6 - 8 tuần):** Methimazole **10 - 15 mg/ngày** (uống 1 lần buổi sáng).")

        st.markdown("---")
        st.markdown("#### 🔄 Quy Trình Đánh Giá Lại & Chỉnh Liều Thuốc Kháng Giáp (ATD Titration Protocol)")
        st.markdown("""
        ##### 📅 1. Lịch Tái Khám & Xét Nghiệm Kiểm Tra Định Kỳ:
        * **Mốc tái khám:** Bệnh nhân tái khám và xét nghiệm lại **FT4 và FT3** sau **4 – 6 tuần** bắt đầu điều trị tấn công.
        * ⚠️ **LƯU Ý VÀNG VỀ TSH:** Trong 2 – 3 tháng đầu điều trị cường giáp, **TSH thường vẫn bị ức chế sâu (< 0.01 mIU/L)** do tuyến yên chưa phục hồi sau thời gian dài bị ức chế. Do đó, **TUYỆT ĐỐI KHÔNG DỰA VÀO TSH ĐỂ TĂNG LIỀU THUỐC KHÁNG GIÁP** khi $FT_4/FT_3$ đã giảm về bình thường. Chỉ số căn cứ chính để chỉnh liều trong giai đoạn này là **$FT_4$ và $FT_3$**.

        ##### 📉 2. Quy Trình Chỉnh Liều Cụ Thể Sau Tái Khám:
        * 🟢 **Trường hợp 1: Khi $FT_4$ và $FT_3$ đã giảm về khoảng bình thường (Đạt Bình Giáp):**
            * **Hành động:** Bắt đầu **giảm liều từ 30% đến 50% liều hiện tại** sau mỗi 4 – 6 tuần.
            * **Sơ đồ giảm liều từng bước (Ví dụ với Methimazole):**
                * *Giai đoạn tấn công:* 30 mg/ngày (dùng 6–8 tuần) -> $FT_4$ về bình thường -> **Giảm xuống 15 mg/ngày** (uống 4–6 tuần).
                * *Lần tái khám tiếp theo:* $FT_4/FT_3$ tiếp tục bình thường -> **Giảm xuống 10 mg/ngày** (uống 4–6 tuần).
                * *Lần tái khám tiếp theo:* $FT_4/TSH$ bình thường -> **Giảm xuống Liều duy trì: 5 – 10 mg/ngày** (hoặc 2.5 – 5 mg/ngày).
            * **Thời gian điều trị duy trì:** Tiếp tục duy trì liều tối thiểu này liên tục trong **12 – 18 tháng**.
        * 🔴 **Trường hợp 2: Khi $FT_4/FT_3$ vẫn còn tăng cao sau 6–8 tuần (Chưa kiểm soát được):**
            * **Hành động:** **Tăng liều (Escalation)** thêm 50% liều ban đầu (Ví dụ: Methimazole 15 mg/ngày -> tăng lên 30 mg/ngày; hoặc 30 mg -> 40 mg/ngày).
            * **Xử trí bổ sung:** Rà soát lại việc tuân thủ dùng thuốc hàng ngày của bệnh nhân, loại trừ các yếu tố thúc đẩy (nhiễm trùng, ngộ độc Iod, căng thẳng tâm lý).
            * **Lịch hẹn:** Hẹn tái khám kiểm tra lại $FT_4/FT_3$ sau **3 – 4 tuần**.
        * 🟡 **Trường hợp 3: Khi $FT_4/FT_3$ giảm thấp dưới mức bình thường (Suy giáp do thuốc):**
            * **Hành động:** **Giảm liều nhanh 50%** hoặc **tạm ngưng thuốc kháng giáp trong 3 – 5 ngày**, sau đó dùng lại với 1/2 liều cũ.

        ##### 🏁 3. Tiêu Chuẩn Đánh Giá Đủ Điều Kiện Ngừng Thuốc Kháng Giáp (Discontinuation Criteria):
        * ✅ Đã hoàn thành đủ tổng thời gian điều trị **12 – 18 tháng**.
        * ✅ Bệnh nhân duy trì bình giáp lâm sàng ổn định với liều duy trì tối thiểu (Methimazole 2.5 – 5 mg/ngày) trong ít nhất 6 tháng.
        * ✅ **Nồng độ $TSH$ đã phục hồi hoàn toàn về khoảng bình thường** (0.4 – 4.5 mIU/L).
        * ✅ **Kháng thể $TRAb$ thử lại đạt kết quả ÂM TÍNH (-)** (Đây là yếu tố tiên lượng quan trọng nhất đảm bảo tỷ lệ tái phát thấp).
        * **Theo dõi sau ngưng thuốc:** Tái khám xét nghiệm $TSH, FT_4$ mỗi **2 – 3 tháng trong năm đầu tiên** sau khi ngừng thuốc để phát hiện sớm các trường hợp tái phát.
        """)

        st.markdown("---")
        # 2. Beta Blockers
        st.markdown("#### 2. Thuốc Kiểm Soát Nhịp Tim & Triệu Chứng Giao Cảm")
        if "Hen phế quản / COPD" in comorbidities or "Suy tim sung huyết" in comorbidities:
            st.error("❌ **CHỐNG CHỈ ĐỊNH CHẸN BETA:** Bệnh nhân có Hen phế quản / COPD hoặc Suy tim nặng.")
            st.markdown("👉 **Thay thế bằng:** Thuốc chẹn kênh Calci nhóm non-dihydropyridine: **Diltiazem** 60 - 120 mg/ngày hoặc **Verapamil**.")
        else:
            st.success("👉 **Lựa chọn hàng đầu: Propranolol** (hoặc Atenolol 25 - 50 mg/ngày)")
            if hr >= 110 or bwps_total >= 25:
                st.markdown("- **Liều ban đầu:** Propranolol **20 - 40 mg mỗi 6 - 8 giờ** (uống).")
                st.markdown("- **Thời gian & Chỉnh liều:** Giảm liều dần và ngưng thuốc khi nhịp tim lúc nghỉ < 90 lần/phút và bệnh nhân đã đạt trạng thái bình giáp bằng thuốc kháng giáp.")
            else:
                st.markdown("- **Liều dùng:** Propranolol 10 - 20 mg x 2-3 lần/ngày khi cần giảm hồi hộp, run tay.")

        # 3. Adjuvant
        st.markdown("#### 3. Thuốc Hỗ Trợ Đặc Biệt")
        col_ad1, col_ad2, col_ad3 = st.columns(3)
        with col_ad1:
            st.markdown("**Corticoid (Glucocorticoid):**")
            if len(eye_exam) > 0 or bwps_total >= 25:
                st.warning("⚠️ **Chỉ định Corticoid:** Prednisone **40 - 60 mg/ngày** (uống trong 2-4 tuần rồi giảm dần liều) hoặc Hydrocortisone IV trong bão giáp/mắt nặng.")
            else:
                st.info("Chưa có chỉ định.")
        with col_ad2:
            st.markdown("**Dung dịch Lugol (Iod vô cơ):**")
            if bwps_total >= 45:
                st.warning("⚠️ **Lugol cấp cứu Bão giáp:** 10 - 20 giọt x 4 lần/ngày (dùng trong 3-5 ngày). *Bắt buộc uống SAU viên PTU đầu tiên ít nhất 1 giờ*.")
            elif "gây chèn ép" in goiter_exam:
                st.info("Dùng Lugol 20-60 giọt/ngày trong 10-14 ngày ngay trước mổ để giảm tưới máu bướu giáp.")
            else:
                st.info("Chưa cần dùng.")
        with col_ad3:
            st.markdown("**Cholestyramine:**")
            if ft4 >= 4.0 or bwps_total >= 25:
                st.warning("⚠️ **Cholestyramine:** 4 g x 4 lần/ngày (dùng trong 2-4 tuần) để ngắt chu trình gan-ruột, giảm nhanh T4/T3.")
            else:
                st.info("Chưa cần dùng.")

    elif diag_category == "THYROIDITIS":
        st.markdown("### 🅱️ PHÁC ĐỒ ĐIỀU TRỊ VIÊM GIÁP BÁN CẤP DE QUERVAIN")
        st.error("⛔ **CẢNH BÁO LÂM SÀNG:** **KHÔNG DÙNG THUỐC KHÁNG GIÁP TỔNG HỢP (Methimazole/PTU)** vì tình trạng nhiễm độc giáp là do phóng thích hormone sẵn có từ nang giáp bị phá hủy, không phải do tăng tổng hợp mới.")
        
        st.markdown("""
        #### 💊 1. Giai Đoạn 1: Kháng Viêm & Giảm Đau (2 – 6 tuần)
        * **Mức độ nhẹ – trung bình (Đau nhẹ, không sốt cao):**
            * **NSAIDs:** **Ibuprofen** 400 – 800 mg x 3 lần/ngày (uống sau ăn) HOẶC **Naproxen** 500 mg x 2 lần/ngày trong **2 – 4 tuần**.
        * **Mức độ nặng (Đau nhiều, sốt cao, không đáp ứng NSAIDs sau 48–72h):**
            * **Prednisone (Corticoid):** **40 mg/ngày** (uống 1 lần buổi sáng) trong **1 – 2 tuần**.
            * **Quy trình giảm liều Prednisone:** Khi bệnh nhân hết đau sốt rõ rệt, giảm liều dần **5 mg mỗi 3 – 5 ngày** (Giảm từ 40mg -> 35mg -> 30mg -> ... -> 5mg -> ngưng). Tổng thời gian dùng Corticoid kéo dài **4 – 6 tuần**.

        #### 🫀 2. Giai Đoạn 2: Kiểm Soát Nhịp Tim & Triệu Chứng Giao Cảm
        * **Propranolol:** **20 – 40 mg x 2 – 3 lần/ngày** trong giai đoạn nhiễm độc giáp (2–6 tuần đầu), sau đó giảm liều và ngưng khi nhịp tim bình thường.

        #### 🔄 3. Giai Đoạn 3: Đánh Giá & Xử Trí Giai Đoạn Suy Giáp Thoáng Qua
        * **Lịch kiểm tra:** Thử lại **TSH và FT4** sau **6 – 8 tuần**.
        * **Xử trí:** Nếu xuất hiện Suy giáp thoáng qua ($TSH > 10\text{ mIU/L}$ hoặc $FT_4$ giảm kèm triệu chứng mệt mỏi), bổ sung tạm thời **Levothyroxine ($LT_4$) 25 – 50 µg/ngày** trong **2 – 3 tháng**, sau đó ngưng thuốc để đánh giá sự phục hồi hoàn toàn của tuyến giáp.
        """)

    elif diag_category == "HYPO":
        st.markdown("### 🅰️ PHÁC ĐỒ ĐIỀU TRỊ SUY GIÁP & SUY GIÁP DƯỚI LÂM SÀNG")
        
        need_lt4 = True
        if "dưới lâm sàng" in primary_diag:
            st.markdown("#### 📋 Chỉ Định Điều Trị Suy Giáp Dưới Lâm Sàng:")
            reasons = []
            if tpo_ab == "Dương tính (+)": reasons.append("Kháng thể **TPO-Ab (+)** (nguy cơ tiến triển thành suy giáp thực sự cao)")
            if len(hypo_symptoms) > 0: reasons.append(f"Có **{len(hypo_symptoms)} triệu chứng** suy giáp rõ")
            if tsh >= 10.0: reasons.append("Nồng độ **TSH ≥ 10 mIU/L**")
            if is_pregnant: reasons.append("Bệnh nhân **đang mang thai** (bắt buộc đảm bảo sự phát triển não bộ thai nhi)")
            
            if len(reasons) > 0:
                need_lt4 = True
                st.success("👉 **CHỈ ĐỊNH DÙNG LEVOTHYROXINE ($LT_4$):**")
                for r in reasons: st.markdown(f"  - ✅ {r}")
            else:
                need_lt4 = False
                st.warning("⚠️ **CHƯA CÓ CHỈ ĐỊNH DÙNG THUỐC NGAY:** TPO-Ab (-), không triệu chứng và TSH < 10 mIU/L. -> **Theo dõi định kỳ TSH/FT4 mỗi 3 - 6 tháng**.")

        if need_lt4:
            st.markdown("#### 💊 Thuốc Ưu Tiên: Levothyroxine ($LT_4$) - Liều Lượng Ban Đầu")
            st.markdown("- **Cơ chế & Động học:** Bổ sung T4 đồng dạng sinh học, thời gian bán hủy dài (~7 ngày), duy trì T4/T3 ổn định, uống 1 lần/ngày.")
            
            st.markdown("##### 📏 Liều Khởi Đầu Cá Thể Hóa:")
            if is_pregnant:
                st.warning("🤰 **Phụ nữ mang thai bị suy giáp / suy giáp dưới lâm sàng:**")
                if tsh < 5.0: st.markdown("- **Liều khởi đầu:** **50 µg/ngày**.")
                elif 5.0 <= tsh <= 8.0: st.markdown("- **Liều khởi đầu:** **75 µg/ngày**.")
                else:
                    d_calc = round(1.6 * weight_kg, 0)
                    st.markdown(f"- **Liều khởi đầu (1.6 µg/kg/ngày):** khoảng **{d_calc} µg/ngày**.")
                st.markdown("- **Nếu đã dùng LT4 trước thai kỳ:** Tăng liều ngay **25 - 30%** khi phát hiện có thai.")
            elif "Người cao tuổi (> 60 tuổi)" in comorbidities or "Bệnh động mạch vành" in comorbidities or age >= 60:
                st.warning("⚠️ **Người cao tuổi / Tiền sử bệnh tim mạch - mạch vành:**")
                st.markdown("- **Liều khởi đầu RẤT THẤP:** **12.5 - 25 µg/ngày** (0.5 - 1 viên 25 µg).")
                st.markdown("- **Quy trình tăng liều:** Tăng chậm từng bước **12.5 - 25 µg sau mỗi 3 - 4 tuần**. Theo dõi sát Điện tâm đồ (ECG) và triệu chứng đau thắt ngực.")
            elif "dưới lâm sàng" in primary_diag:
                st.info("- **Suy giáp dưới lâm sàng (người trẻ):** Khởi đầu **25 - 50 µg/ngày**.")
            else:
                full_d = round(1.6 * weight_kg, 0)
                st.success(f"- **Suy giáp lâm sàng (người trẻ khỏe mạnh):** Liều khởi đầu **25 - 50 µg/ngày**, tăng dần mỗi 25-50 µg sau 2-3 tuần. Liều duy trì ước tính (~1.6 µg/kg/ngày) khoảng **{full_d} µg/ngày**.")

            st.markdown("---")
            st.markdown("#### 🔄 Quy Trình Tái Khám & Chỉnh Liều Levothyroxine ($LT_4$ Titration Protocol)")
            st.markdown("""
            ##### 📅 1. Lịch Tái Khám & Xét Nghiệm Kiểm Tra:
            * **Mốc kiểm tra:** Tái khám xét nghiệm **TSH và FT4** sau **6 – 8 tuần** kể từ khi bắt đầu uống thuốc hoặc thay đổi liều $LT_4$.

            ##### 📈 2. Quy Trình Điều Chỉnh Liều Cụ Thể Sau Tái Khám:
            * 🔴 **Trường hợp TSH > Mục tiêu (> 4.5 mIU/L, hoặc > mục tiêu quý thai kỳ):**
                * **Hành động (Tăng liều - Escalation):** Tăng liều $LT_4$ thêm **12.5 – 25 µg/ngày** (ở người cao tuổi / bệnh tim) hoặc tăng thêm **25 – 50 µg/ngày** (ở người trẻ khỏe mạnh).
                * **Lịch hẹn:** Kiểm tra lại $TSH$ và $FT_4$ sau **6 – 8 tuần**.
            * 🟡 **Trường hợp TSH < Mục tiêu (< 0.4 mIU/L - Quá liều $LT_4$ / Cường giáp do thuốc):**
                * **Hành động (Giảm liều):** Giảm liều $LT_4$ đi **12.5 – 25 µg/ngày**.
                * **Lịch hẹn:** Kiểm tra lại $TSH$ và $FT_4$ sau **6 – 8 tuần**.
            * 🟢 **Trường hợp TSH Đạt Mục Tiêu (0.5 – 2.5 mIU/L ở người trẻ; 1.0 – 3.0 mIU/L ở người cao tuổi):**
                * **Hành động:** **Duy trì nguyên liều $LT_4$ hiện tại**.
                * **Lịch theo dõi lâu dài:** Tái khám thử $TSH$ và $FT_4$ định kỳ mỗi **6 – 12 tháng** (Đối với phụ nữ mang thai: thử $TSH$ mỗi **4 tuần** cho đến tuần thứ 20 thai kỳ, và ít nhất 1 lần ở tuần thứ 30).

            ##### ⏰ 3. Cách Uống Thuốc $LT_4$ Chuẩn Xác:
            * Uống vào **buổi sáng khi bụng trống**, trước bữa ăn sáng **30 – 60 phút** với nhiều nước lọc (hoặc trước đi ngủ sau ăn tối > 2 giờ).
            * Uống cách xa ít nhất **4 giờ** đối với các thuốc chứa Sắt, Canxi, Antacid chứa Nhôm/Magie hoặc Cholestyramine do làm giảm hấp thu $LT_4$.
            """)

    else:
        st.success("✅ **CHỨC NĂNG GIÁP TRONG GIỚI HẠN BÌNH THƯỜNG (BÌNH GIÁP)**")
        st.markdown("- Không có chỉ định điều trị bằng thuốc.")

# ==========================================
# TAB 5: PHÂN TÍCH CASE LÂM SÀNG & CƠ CHẾ
# ==========================================
with tab_case_study:
    st.subheader("🧬 Phân Tích Case Lâm Sàng Cụ Thể, Giải Phẫu, Sinh Lý Bệnh & Dược Lý Thuốc")
    
    st.markdown(f"""
    <div class="section-box">
        <h4>📋 TÓM TẮT CASE LÂM SÀNG ĐANG PHÂN TÍCH</h4>
        <ul>
            <li><b>Bệnh nhân:</b> {patient_name}, {gender}, {age} tuổi, Cân nặng: {weight_kg} kg. {f'(Mang thai {preg_trimester})' if is_pregnant else ''}</li>
            <li><b>Tiền sử / Bệnh nền:</b> {', '.join(comorbidities) if len(comorbidities)>0 else 'Chưa ghi nhận bệnh nền đặc biệt'}.</li>
            <li><b>Lâm sàng nổi bật:</b> Nhịp tim {hr} bpm, Thân nhiệt {temp} °C, Thay đổi cân nặng {weight_change} kg. Tiêu hóa: {stool_freq}. Thần kinh: {cns_status}. Bướu giáp: {goiter_exam}. Mắt: {', '.join(eye_exam) if len(eye_exam)>0 else 'Bình thường'}.</li>
            <li><b>Cận lâm sàng & Cụ thể:</b> TSH = <b>{tsh}</b> mIU/L, FT4 = <b>{ft4}</b> ng/dL, FT3 = <b>{ft3}</b> pg/mL. Kháng thể TRAb = <b>{trab}</b>, TPO-Ab = <b>{tpo_ab}</b>. ANC = {anc}/mm³, ALT = {alt} U/L. Điểm BWPS = <b>{bwps_total} điểm</b>.</li>
            <li><b>Chẩn đoán xác định:</b> <span style="color:#2563EB; font-weight:bold;">{primary_diag}</span>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_phys, col_patho = st.columns(2)
    
    with col_phys:
        st.markdown("### 1. Giải Phẫu & Sinh Lý Trục Hạ Đồi - Tuyến Yên - Tuyến Giáp (Trục HPT)")
        st.markdown("""
        * **Giải phẫu & Cấp máu Tuyến giáp:** Tuyến giáp gồm 2 thùy nối nhau bởi eo giáp, nằm trước sụn nhẫn và các vòng sụn khí quản đầu tiên. Tuyến giáp được cấp máu cực kỳ giàu có bởi **Động mạch giáp trên** (nhánh ĐM cảnh ngoài) và **Động mạch giáp dưới** (nhánh thân giáp cổ của ĐM dưới đòn). Khi tuyến giáp bị kích thích tăng sinh mạch máu mạnh (như trong Basedow), lưu lượng máu tăng gấp nhiều lần tạo ra **tiếng thổi tâm thu/liên tục (bướu mạch)** và hình ảnh **"Thyroid Inferno"** trên siêu âm Doppler.
        * **Sinh hóa Tổng hợp Hormone Giáp:**
            1. **Bắt Iod (Iodide Trapping):** Bơm đồng vận $Na^+/I^-$ (NIS) ở màng đáy tế bào nang giáp vận chuyển tích cực $I^-$ từ máu vào tế bào.
            2. **Oxy hóa & Hữu cơ hóa:** Enzyme **Thyroid Peroxidase (TPO)** ở màng đỉnh oxy hóa $I^-$ thành $I_2$ và gắn Iod vào các gốc Tyrosine của khung protein **Thyroglobulin (Tg)** tạo thành **MIT** (Monoiodotyrosine) và **DIT** (Diiodotyrosine).
            3. **Ngưng kết (Coupling):** Men TPO gắn ngưng kết `MIT + DIT -> T3` và `DIT + DIT -> T4`.
            4. **Phóng thích:** Hormone trữ trong lòng nang giáp dưới dạng Keo giáp (Colloid). Khi có kích thích của TSH, tế bào tái hấp thu Tg, thủy phân giải phóng $T_4$ và $T_3$ tự do vào máu.
        * **Trục HPT & Feed-back Âm:** Trùng Hạ đồi tiết TRH -> Kích thích Tuyến yên tiết TSH -> Kích thích Tuyến giáp tiết T4 & T3. Nồng độ FT4/FT3 tự do trong máu tăng cao sẽ tác động **Feedback âm trực tiếp lên Tuyến yên và Hạ đồi**, làm ức chế gần như hoàn toàn sự tiết TSH (dẫn đến chỉ số $TSH < 0.01\\text{ mIU/L}$).
        """)

    with col_patho:
        st.markdown("### 2. Cơ Chế Sinh Lý Bệnh Cụ Thể Của Case Lâm Sàng")
        if diag_category == "HYPER" and "Basedow" in primary_diag:
            st.markdown("""
            * **Tự miễn trong Bệnh Basedow:** Do sự mất dung nạp tự miễn, cơ thể sản xuất tự kháng thể **TRAb (TSH Receptor Antibody)**, đặc biệt là thể kích thích **TSI (Thyroid Stimulating Immunoglobulin)**. 
            * **Cơ chế gây Cường giáp:** Kháng thể TRAb gắn trực tiếp và kích hoạt liên tục thụ thể TSH (TSHR) trên màng tế bào nang giáp mà không phụ thuộc vào cơ chế kiểm soát feed-back của cơ thể. TSHR bị kích hoạt liên tục -> Tăng sản xuất cAMP nội bào -> Tăng sinh phì đại tế bào giáp, tăng bắt Iod và phóng thích ồ ạt $T_4, T_3$ vào máu gây **Hội chứng Nhiễm độc giáp**.
            * **Cơ chế Bệnh mắt Basedow (Orbitopathy):** Thụ thể TSHR và chất nguyên bào sợi còn biểu hiện ở mô liên kết sau hốc mắt. Kháng thể TRAb cùng tế bào T thâm nhiễm vào hốc mắt, kích thích nguyên bào sợi sản xuất lượng lớn **Glycosaminoglycans (GAGs / Hyaluronic acid)** có tính chất háo nước mạnh -> Gây phù nề, tăng thể tích mô mỡ và cơ vận nhãn sau hốc mắt -> Đẩy nhãn cầu ra trước (**Lồi mắt**), chèn ép cơ vận nhãn (nhìn đôi) và nguy cơ chèn ép thần kinh thị.
            """)
        elif diag_category == "THYROIDITIS":
            st.markdown("""
            * **Cơ chế Viêm giáp bán cấp de Quervain:** Thường xuất hiện sau một đợt nhiễm virus đường hô hấp trên. Phản ứng miễn dịch/viêm hạt đáp ứng với virus tấn công và phá hủy cấu trúc tế bào nang giáp.
            * **Giải phóng Hormone thụ động:** Nang giáp bị vỡ làm toàn bộ kho keo giáp chứa $T_4, T_3$ dự trữ **thoát ồ ạt vào máu**, gây nhiễm độc giáp cấp tính.
            * **Giải thích Cận lâm sàng:**
                - *Tổn thương vỡ nang:* Tuyến giáp bị viêm không còn khả năng bắt Iod -> **Độ tập trung 131-I giảm cực thấp (< 1-2%)**.
                - *Phản ứng viêm toàn thân:* Chỉ số **CRP / ESR tăng rất cao**, bệnh nhân có sốt và đau nhức tuyến giáp rõ rệt.
            """)
        elif diag_category == "HYPO":
            st.markdown("""
            * **Cơ chế Viêm giáp tự miễn Hashimoto:** Cơ thể sinh ra các tự kháng thể **Anti-TPO (TPO-Ab)** và **Anti-Tg**.
            * **Phá hủy nang giáp mạn tính:** Kháng thể cùng các tế bào T độc ($CD8^+$) thâm nhiễm phá hủy tế bào nang giáp tiến triển, làm giảm dần khả năng tổng hợp hormone giáp.
            * **Tiến triển từ Dưới lâm sàng đến Lâm sàng:** Ban đầu, khi tế bào giáp bắt đầu suy giảm, Tuyến yên sẽ phản ứng bù trừ bằng cách **tăng tiết TSH** để kích thích phần mô giáp còn lại (Giai đoạn Suy giáp dưới lâm sàng: $TSH$ tăng, $FT_4$ bình thường). Khi sự phá hủy lan rộng vượt quá khả năng bù trừ, $FT_4$ giảm thấp dẫn đến Suy giáp lâm sàng.
            """)
        else:
            st.markdown("* Chức năng tuyến giáp trong giới hạn bình thường. Trục HPT hoạt động cân bằng sinh lý.")

    st.markdown("---")
    st.markdown("### 3. Cơ Chế Tác Động Dược Lý Của Các Thuốc Trong Phác Đồ")
    
    col_drug1, col_drug2 = st.columns(2)
    
    with col_drug1:
        st.markdown("""
        ##### 💊 1. Thuốc Kháng Giáp Tổng Hợp (Methimazole & PTU)
        * **Cơ chế phân tử:** Cả Methimazole và Propylthiouracil (PTU) đều là chất gắn cạnh tranh và ức chế enzyme **Thyroid Peroxidase (TPO)** ở màng đỉnh tế bào nang giáp.
        * **Tác động:** Khóa quá trình oxy hóa $I^-$ thành $I_2$, ngăn sự hữu cơ hóa Iod vào gốc Tyrosine và ngăn sự ngưng kết MIT/DIT -> **Chặn hoàn toàn sự tổng hợp hormone giáp mới**.
        * **Điểm khác biệt của PTU:** Ở liều cao, PTU còn có thêm khả năng ức chế enzyme **5'-deiodinase ngoại vi** ở gan và thận, giúp ngăn cản sự chuyển đổi từ $T_4$ (ít hoạt tính) thành $T_3$ (dạng hormone hoạt tính mạnh gấp 4 lần) -> Rất có lợi trong **Cơn bão giáp**.
        * **Thời gian tác dụng:** Thuốc chỉ chặn tổng hợp hormone mới, không phân hủy hormone đã tích trữ sẵn trong lòng nang giáp. Do đó, cần **3 – 4 tuần** điều trị tấn công để dùng hết kho dự trữ $T_4/T_3$ thì nồng độ hormone giáp trong máu mới bắt đầu giảm rõ.

        ##### 🫀 2. Thuốc Chẹn Beta Giao Cảm (Propranolol)
        * **Cơ chế:** Phong lập cạnh tranh thụ thể $\\beta_1$ và $\\beta_2$ adrenergic của hệ thần kinh giao cảm.
        * **Tác động:** Giảm nhanh chóng các triệu chứng kích thích giao cảm do tăng nhạy cảm Catecholamine trong cường giáp: giảm nhịp tim nhanh, giảm rung nhĩ, giảm hồi hộp đánh trống ngực, giảm run tay và giảm vã mồ hôi.
        * **Tác động ngoại vi:** Propranolol liều cao (> 160 mg/ngày) cũng ức chế nhẹ men 5'-deiodinase ngoại vi, hỗ trợ làm giảm $T_3$ máu.
        """)
        
    with col_drug2:
        st.markdown("""
        ##### 🩸 3. Dung Dịch Lugol (Iod Vô Cơ Liều Cao)
        * **Hiệu ứng Wolff-Chaikoff:** Nồng độ Iod vô cơ tự do trong máu tăng đột ngột liều cao sẽ gây ra hiện tượng tự ức chế tạm thời sự hữu cơ hóa Iod và **khóa ngay lập tức sự phóng thích $T_4, T_3$ từ nang giáp vào máu**.
        * **Tác dụng vascular:** Giảm dòng máu cấp cho tuyến giáp, làm tuyến giáp săn chắc và giảm tưới máu rõ rệt -> Ứng dụng quan trọng trước phẫu thuật cắt giáp 10-14 ngày.
        * **Lưu ý thời điểm:** Phải cho Lugol **SAU khi đã dùng thuốc KGTH (PTU/Methimazole) ít nhất 1 giờ** để đảm bảo men TPO đã bị khóa, tránh việc tuyến giáp sử dụng lượng Iod vô cơ này làm nguyên liệu tổng hợp thêm hormone.

        ##### 💊 4. Levothyroxine ($LT_4$) trong Điều Trị Suy Giáp
        * **Cơ chế:** Cung cấp L-thyroxine đồng dạng sinh học hệt như $T_4$ nội sinh do tuyến giáp tiết ra.
        * **Chuyển hóa:** $LT_4$ ngoại nguồn vào cơ thể sẽ được enzym 5'-deiodinase ở mô ngoại vi (gan, thận, não) deiodin hóa loại bỏ 1 nguyên tử Iod ở vòng ngoài để chuyển thành $T_3$ hoạt tính sinh học theo đúng nhu cầu sinh lý của cơ thể.
        * **Động học dài hạn:** $LT_4$ gắn kết rất mạnh với protein gắn giáp (TBG) trong máu, mang lại **thời gian bán hủy ($T_{1/2}$) kéo dài đến 7 ngày**, giúp duy trì nồng độ hormone vô cùng ổn định chỉ với 1 liều uống duy nhất trong ngày.
        """)

st.markdown("---")
st.caption("Ứng dụng được xây dựng theo chuẩn mực chuyên môn Y khoa Nội tiết - Đại học Y Dược TP.HCM và các Guideline Quốc tế ATA/ETA.")
