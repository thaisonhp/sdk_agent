from agents import function_tool

@function_tool
def calculate_pit_in_vn(income : float, money_type : str, vietnamese :bool, dependent_count : int, dependent_months : int , bhxh : float)->float:

    
    """
    Hàm tính thuế TNCN tại Việt Nam dựa trên thông tin từ pit_agent.
    Đầu vào:
        - income: Tổng thu nhập (VND)
        - money_type: "month" (theo tháng) hoặc "year" (theo năm)
        - vietnamese: True (người VN, giả định cư trú) hoặc False (người nước ngoài, giả định không cư trú)
        - dependent_count: Số lượng người phụ thuộc
        - dependent_months: Tổng số tháng phụ thuộc trong năm
        - bhxh: Mức lương đóng bảo hiểm xã hội (VND)
    Đầu ra:
        - Số thuế TNCN phải nộp (VND)
    """
    
    # Mức giảm trừ gia cảnh
    giam_tru_ban_than = 11_000_000  # Mỗi tháng
    giam_tru_nguoi_phu_thuoc = 4_400_000  # Mỗi người mỗi tháng
    
    # Điều chỉnh thu nhập và bảo hiểm theo tháng hoặc năm
    if money_type == "year":
        thu_nhap_thang = income / 12
        luong_dong_bao_hiem_thang = bhxh / 12
        # Giảm trừ gia cảnh bản thân cho cả năm (12 tháng)
        giam_tru_ban_than_ca_nam = giam_tru_ban_than * 12
        # Giảm trừ gia cảnh người phụ thuộc dựa trên tổng số tháng phụ thuộc
        giam_tru_nguoi_phu_thuoc_ca_nam = giam_tru_nguoi_phu_thuoc * dependent_months
    else:  # money_type == "month"
        thu_nhap_thang = income
        luong_dong_bao_hiem_thang = bhxh
        # Giảm trừ gia cảnh bản thân cho 1 tháng
        giam_tru_ban_than_ca_nam = giam_tru_ban_than
        # Giảm trừ gia cảnh người phụ thuộc cho 1 tháng (giả định dependent_months là số tháng trong tháng đó)
        giam_tru_nguoi_phu_thuoc_ca_nam = giam_tru_nguoi_phu_thuoc * dependent_count
    
    # Trường hợp không cư trú (giả định vietnamese = False)
    if not vietnamese:
        thue = thu_nhap_thang * 0.20  # Thuế suất cố định 20%
        return round(thue * (12 if money_type == "year" else 1))
    
    # Trường hợp cư trú (giả định vietnamese = True)
    # Tính bảo hiểm bắt buộc (theo tháng)
    bhxh_thang = min(luong_dong_bao_hiem_thang, 36_000_000) * 0.08  # 8%
    bhyt_thang = min(luong_dong_bao_hiem_thang, 36_000_000) * 0.015  # 1.5%
    bhtn_thang = min(luong_dong_bao_hiem_thang, 93_600_000) * 0.01  # 1%
    tong_bao_hiem_thang = bhxh_thang + bhyt_thang + bhtn_thang
    
    # Tổng bảo hiểm cho toàn kỳ (năm hoặc tháng)
    tong_bao_hiem = tong_bao_hiem_thang * (12 if money_type == "year" else 1)
    
    # Tổng giảm trừ (bao gồm gia cảnh và bảo hiểm)
    if money_type == "year":
        tong_giam_tru = giam_tru_ban_than_ca_nam + giam_tru_nguoi_phu_thuoc_ca_nam + tong_bao_hiem
        thu_nhap_tinh_thue = max(income - tong_giam_tru, 0)
    else:
        tong_giam_tru = giam_tru_ban_than_ca_nam + giam_tru_nguoi_phu_thuoc_ca_nam + tong_bao_hiem
        thu_nhap_tinh_thue = max(thu_nhap_thang - tong_giam_tru, 0)
    
    # Biểu thuế lũy tiến từng phần (tính trên thu nhập tháng)
    if money_type == "year":
        thu_nhap_tinh_thue_thang = thu_nhap_tinh_thue / 12
    else:
        thu_nhap_tinh_thue_thang = thu_nhap_tinh_thue
    
    thue_thang = 0
    if thu_nhap_tinh_thue_thang <= 0:
        thue_thang = 0
    elif thu_nhap_tinh_thue_thang <= 5_000_000:
        thue_thang = thu_nhap_tinh_thue_thang * 0.05
    elif thu_nhap_tinh_thue_thang <= 10_000_000:
        thue_thang = 5_000_000 * 0.05 + (thu_nhap_tinh_thue_thang - 5_000_000) * 0.10
    elif thu_nhap_tinh_thue_thang <= 18_000_000:
        thue_thang = 5_000_000 * 0.05 + 5_000_000 * 0.10 + (thu_nhap_tinh_thue_thang - 10_000_000) * 0.15
    elif thu_nhap_tinh_thue_thang <= 32_000_000:
        thue_thang = 5_000_000 * 0.05 + 5_000_000 * 0.10 + 8_000_000 * 0.15 + (thu_nhap_tinh_thue_thang - 18_000_000) * 0.20
    elif thu_nhap_tinh_thue_thang <= 52_000_000:
        thue_thang = 5_000_000 * 0.05 + 5_000_000 * 0.10 + 8_000_000 * 0.15 + 14_000_000 * 0.20 + (thu_nhap_tinh_thue_thang - 32_000_000) * 0.25
    elif thu_nhap_tinh_thue_thang <= 80_000_000:
        thue_thang = 5_000_000 * 0.05 + 5_000_000 * 0.10 + 8_000_000 * 0.15 + 14_000_000 * 0.20 + 20_000_000 * 0.25 + (thu_nhap_tinh_thue_thang - 52_000_000) * 0.30
    else:
        thue_thang = 5_000_000 * 0.05 + 5_000_000 * 0.10 + 8_000_000 * 0.15 + 14_000_000 * 0.20 + 20_000_000 * 0.25 + 28_000_000 * 0.30 + (thu_nhap_tinh_thue_thang - 80_000_000) * 0.35
    
    # Tổng thuế cho kỳ (năm hoặc tháng)
    thue = thue_thang * (12 if money_type == "year" else 1)
    return round(thue)
