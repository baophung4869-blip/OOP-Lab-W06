"""
/****************/
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
/****************/
"""
from datetime import datetime, timedelta
from borrowing import BorrowingSlip, Lecturer
from devices import AirConditionerRemote, Microphone, ProjectorRemote


def main():
    print("=" * 63)
    print(" BÀI THỰC HÀNH LAB W06: HỆ THỐNG QUẢN LÝ THIẾT BỊ GIẢNG DẠY")
    print(" SV: Phùng Ngọc Bảo - MSSV: 20237303")
    print("=" * 63)

    today = datetime.now()

    # 11.1. LUỒNG THÀNH CÔNG
    print("\n>>> 1. CHẠY KỊCH BẢN KIỂM THỬ THÀNH CÔNG <<<")
    gv = Lecturer("GV001", "TS. Nguyễn Văn A")
    dk_chieu = ProjectorRemote("DKMC01", "Điều khiển Sony", 2024, 300_000.0)
    dk_dieu_hoa = AirConditionerRemote("DKDH01", "Điều khiển Panasonic", 2023, 200_000.0)
    mic = Microphone("MIC01", "Micro Shure không dây", 2023, 1_500_000.0, is_wireless=True)

    slip_ok = BorrowingSlip("PM-001", gv, "Phòng 302-D9", today)
    slip_ok.add_device(dk_chieu, borrow_days=1)
    slip_ok.add_device(mic, borrow_days=1)
    print(f"[OK] Đã tạo phiếu {slip_ok.slip_id} cho GV {gv.full_name} mượn 2 thiết bị.")

    fee_chieu = slip_ok.return_device("DKMC01", today + timedelta(days=1))
    print(f"[OK] Trả DKMC01 đúng hạn. Phí phạt: {fee_chieu:,.0f} VND.")

    fee_mic = slip_ok.return_device("MIC01", today + timedelta(days=3))
    print(f"[OK] Trả MIC01 trễ 2 ngày. Phí phạt: {fee_mic:,.0f} VND.")
    print(f"Tổng tiền phạt của phiếu: {slip_ok.calculate_total_late_fee():,.0f} VND.")


if __name__ == "__main__":
    main()