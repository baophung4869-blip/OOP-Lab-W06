
"""
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional


class DeviceStatus(Enum):
    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "UnderMaintenance"
    Retired = "Retired"


class Device(ABC):
    """Lớp cơ sở trừu tượng đại diện cho thiết bị trường học."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")

        if not isinstance(device_name, str) or not device_name.strip():
            raise ValueError("Tên thiết bị không được để trống.")

        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")

        current_year = datetime.now().year
        if year_of_usage > current_year:
            raise ValueError(
                f"Năm sử dụng không được lớn hơn năm hiện tại ({current_year})."
            )

        if not isinstance(status, DeviceStatus):
            raise ValueError("Trạng thái thiết bị không hợp lệ.")

        self._device_id = device_id.strip()
        self.device_name = device_name.strip()
        self._year_of_usage = year_of_usage
        self._purchase_price = purchase_price
        self.status = status

    @property
    def device_id(self) -> str:
        """Mã thiết bị chỉ đọc."""
        return self._device_id

    @property
    def year_of_usage(self) -> int:
        return self._year_of_usage

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        """Tính chi phí bảo trì dự kiến trong một năm."""
        pass

    def __str__(self) -> str:
        return (
            f"[{self.device_id}] {self.device_name} "
            f"| Năm SD: {self.year_of_usage} "
            f"| Giá: {self.purchase_price:,.0f} VND "
            f"| Trạng thái: {self.status.value}"
        )


class TeachingDevice(Device):
    """Lớp trừu tượng cho thiết bị giảng dạy."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        max_borrow_days: int = 1,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        super().__init__(
            device_id,
            device_name,
            year_of_usage,
            purchase_price,
            status,
        )

        if max_borrow_days <= 0:
            raise ValueError("Số ngày mượn tối đa phải lớn hơn 0.")

        self.max_borrow_days = max_borrow_days

    def mark_as_borrowed(self) -> None:
        if self.status == DeviceStatus.Retired:
            raise ValueError("Không thể mượn thiết bị đã thanh lý.")
        if self.status == DeviceStatus.UnderMaintenance:
            raise ValueError("Không thể mượn thiết bị đang bảo trì.")

        self.status = DeviceStatus.Borrowed

    def mark_as_available(self) -> None:
        if self.status != DeviceStatus.Retired:
            self.status = DeviceStatus.Available

    def set_maintenance(self) -> None:
        if self.status != DeviceStatus.Retired:
            self.status = DeviceStatus.UnderMaintenance


class AirConditionerRemote(TeachingDevice):
    """Điều khiển điều hòa."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        super().__init__(
            device_id,
            device_name,
            year_of_usage,
            purchase_price,
            max_borrow_days=1,
            status=status,
        )

    def calculate_annual_maintenance_cost(self) -> float:
        # 5% giá mua + 50.000 VND tiền pin
        return self.purchase_price * 0.05 + 50_000


class Microphone(TeachingDevice):
    """Micro giảng dạy có dây hoặc không dây."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        is_wireless: bool = True,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        super().__init__(
            device_id,
            device_name,
            year_of_usage,
            purchase_price,
            max_borrow_days=1,
            status=status,
        )
        self.is_wireless = is_wireless

    def calculate_annual_maintenance_cost(self) -> float:
        cost = self.purchase_price * 0.08

        if self.is_wireless:
            cost += 100_000

        return cost


class ProjectorRemote(TeachingDevice):
    """Điều khiển máy chiếu."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        super().__init__(
            device_id,
            device_name,
            year_of_usage,
            purchase_price,
            max_borrow_days=1,
            status=status,
        )

    def calculate_annual_maintenance_cost(self) -> float:
        return self.purchase_price * 0.04


class ClassRoom:
    """Phòng học quản lý danh sách thiết bị theo quan hệ kết tập."""

    def __init__(self, room_id: str, room_name: str, capacity: int):
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")

        if not isinstance(room_name, str) or not room_name.strip():
            raise ValueError("Tên phòng không được để trống.")

        if capacity <= 0:
            raise ValueError("Sức chứa phòng phải lớn hơn 0.")

        self.room_id = room_id.strip()
        self.room_name = room_name.strip()
        self.capacity = capacity
        self._devices: List[Device] = []

    @property
    def devices(self) -> List[Device]:
        """Trả về bản sao danh sách để tránh sửa trực tiếp danh sách nội bộ."""
        return self._devices.copy()

    def add_device(self, device: Device) -> bool:
        """Thêm thiết bị nếu không null, không trùng mã và còn chỗ."""

        if device is None:
            raise ValueError("Không chấp nhận thiết bị None.")

        if not isinstance(device, Device):
            raise TypeError("Đối tượng thêm vào phải là một thiết bị.")

        # Không cho phép trùng mã thiết bị, không phân biệt chữ hoa/thường.
        if self.find_device(device.device_id) is not None:
            return False

        if len(self._devices) >= self.capacity:
            raise ValueError("Phòng học đã đạt sức chứa tối đa.")

        self._devices.append(device)
        return True

    def remove_device(self, device_id: str) -> bool:
        """Xóa thiết bị theo mã. Trả về True nếu xóa thành công."""

        device = self.find_device(device_id)

        if device is None:
            return False

        self._devices.remove(device)
        return True

    def find_device(self, device_id: str) -> Optional[Device]:
        """Tìm thiết bị theo mã, không phân biệt chữ hoa/thường."""

        if not isinstance(device_id, str) or not device_id.strip():
            return None

        target = device_id.strip().lower()

        for device in self._devices:
            if device.device_id.lower() == target:
                return device

        return None

    def calculate_annual_maintenance_cost(self) -> float:
        """Tính tổng chi phí bằng tính đa hình."""

        return sum(
            device.calculate_annual_maintenance_cost()
            for device in self._devices
        )

    def get_devices_requiring_maintenance(self) -> List[Device]:
        """Lọc thiết bị đang bảo trì hoặc đã sử dụng trên 5 năm."""

        current_year = datetime.now().year

        return [
            device
            for device in self._devices
            if (
                device.status == DeviceStatus.UnderMaintenance
                or current_year - device.year_of_usage > 5
            )
        ]

    def __str__(self) -> str:
        return (
            f"Phòng: {self.room_id} - {self.room_name} "
            f"| Sức chứa: {self.capacity} "
            f"| Số thiết bị: {len(self._devices)}"
        )


def main():
    """Chạy thử các chức năng chính."""

    remote = AirConditionerRemote(
        "AC001", "Điều khiển điều hòa", 2022, 300_000
    )

    microphone = Microphone(
        "MIC001", "Micro không dây", 2019, 2_000_000,
        is_wireless=True,
    )

    projector_remote = ProjectorRemote(
        "PRJ001", "Điều khiển máy chiếu", 2020, 500_000
    )

    room = ClassRoom("P101", "Phòng học 101", 5)

    print("=== THÊM THIẾT BỊ ===")
    print("Thêm remote:", room.add_device(remote))
    print("Thêm micro:", room.add_device(microphone))
    print("Thêm remote máy chiếu:", room.add_device(projector_remote))

    # Kiểm tra mã thiết bị trùng.
    duplicate = Microphone(
        "MIC001", "Micro trùng mã", 2023, 1_000_000
    )
    print("Thêm thiết bị trùng mã:", room.add_device(duplicate))

    print("\n=== THÔNG TIN PHÒNG HỌC ===")
    print(room)

    print("\n=== DANH SÁCH THIẾT BỊ ===")
    for device in room.devices:
        print(device)
        print(
            f"Chi phí bảo trì năm: "
            f"{device.calculate_annual_maintenance_cost():,.0f} VND"
        )

    print(
        "\nTổng chi phí bảo trì năm: "
        f"{room.calculate_annual_maintenance_cost():,.0f} VND"
    )

    print("\n=== THIẾT BỊ CẦN BẢO TRÌ ===")
    devices_to_maintain = room.get_devices_requiring_maintenance()

    if devices_to_maintain:
        for device in devices_to_maintain:
            print(device)
    else:
        print("Không có thiết bị cần bảo trì.")

    print("\n=== KIỂM TRA MƯỢN TRẢ ===")
    microphone.mark_as_borrowed()
    print("Sau khi mượn:", microphone.status.value)

    microphone.mark_as_available()
    print("Sau khi trả:", microphone.status.value)

    print("\n=== TÌM VÀ XÓA THIẾT BỊ ===")
    found = room.find_device("mic001")
    print("Tìm MIC001:", found if found else "Không tìm thấy")

    print("Xóa AC001:", room.remove_device("AC001"))
    print(room)


if __name__ == "__main__":
    main()
