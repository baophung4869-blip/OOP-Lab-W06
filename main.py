"""
/****************/
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
/****************/
"""
from datetime import datetime, timedelta
from borrowing import BorrowingSlip, Lecturer, TeachingAssistant
from devices import AirConditionerRemote, Microphone, ProjectorRemote
from exceptions import BorrowingException


def run_test_case(test_name: str, action):
    print(f"\n--- Kiểm thử: {test_name} ---")
    try:
        action()
        print("[Thất bại] Không phát sinh ngoại lệ như kỳ vọng!")
    except BorrowingException as ex:
        print(f"[Bắt ngoại lệ thành công] {type(ex).__name__}: {ex}")
    except ValueError as ex:
        print(f"[Bắt ngoại lệ thành công] ValueError: {ex}")


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

    # 11.2. LUỒNG PHÁT SINH NGOẠI LỆ
    print("\n>>> 2. CHẠY KỊCH BẢN KIỂM THỬ NGOẠI LỆ <<<")
    ta = TeachingAssistant("TA001", "Trợ giảng Trần Thị B")
    slip_test = BorrowingSlip("PM-002", ta, "Phòng 201-B1", today)

    # 1. Mượn điều khiển điều hòa đang UnderMaintenance[cite: 8]
    def test_1():
        broken = AirConditionerRemote("DKDH02", "Điều khiển Daikin", 2023, 200_000.0)
        broken.set_maintenance()
        slip_test.add_device(broken, 1)

    run_test_case("1. Mượn thiết bị đang UnderMaintenance", test_1)

    # 2. Thêm cùng một micro hai lần[cite: 8]
    def test_2():
        mic_dup = Microphone("MIC02", "Micro có dây", 2024, 500_000.0, False)
        slip_test.add_device(mic_dup, 1)
        slip_test.add_device(mic_dup, 1)

    run_test_case("2. Thêm cùng một micro hai lần vào phiếu", test_2)

    # 3. Trợ giảng mượn thiết bị thứ ba (Vượt hạn mức 2)[cite: 3, 8]
    def test_3():
        slip_over = BorrowingSlip("PM-OVER", ta, "Phòng Lab 2", today)
        slip_over.add_device(ProjectorRemote("DKMC02", "Sony", 2024, 250_000.0), 1)
        slip_over.add_device(AirConditionerRemote("DKDH03", "LG", 2024, 180_000.0), 1)
        slip_over.add_device(Microphone("MIC03", "Mic", 2024, 600_000.0, False), 1)

    run_test_case("3. Trợ giảng mượn thiết bị thứ 3 (Vượt hạn mức 2)", test_3)

    # 4. Mượn micro trong 3 ngày dù giới hạn là 1 ngày[cite: 8]
    def test_4():
        slip_test.add_device(Microphone("MIC04", "Mic", 2024, 700_000.0, False), borrow_days=3)

    run_test_case("4. Mượn micro 3 ngày (Tối đa 1 ngày)", test_4)

    # 5. Trả thiết bị không thuộc phiếu mượn[cite: 8]
    def test_5():
        slip_test.return_device("NOT_EXIST", today)

    run_test_case("5. Trả thiết bị không thuộc phiếu mượn", test_5)

    # 6. Trả cùng một thiết bị hai lần[cite: 8]
    def test_6():
        dev = ProjectorRemote("DKMC03", "Panasonic", 2024, 300_000.0)
        s = BorrowingSlip("PM-003", gv, "P105", today)
        s.add_device(dev, 1)
        s.return_device("DKMC03", today)
        s.return_device("DKMC03", today)

    run_test_case("6. Trả cùng một thiết bị hai lần", test_6)

    # 7. Trả thiết bị với ngày trả trước ngày mượn[cite: 8]
    def test_7():
        dev = ProjectorRemote("DKMC04", "ViewSonic", 2024, 300_000.0)
        s = BorrowingSlip("PM-004", gv, "P106", today)
        s.add_device(dev, 1)
        s.return_device("DKMC04", today - timedelta(days=2))

    run_test_case("7. Ngày trả trước ngày mượn", test_7)

    print("\nHoàn tất toàn bộ kịch bản kiểm thử!")


if __name__ == "__main__":
    main()