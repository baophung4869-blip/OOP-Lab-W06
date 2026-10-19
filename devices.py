"""
/****************/
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
/****************/
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


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
        if not device_id or not device_id.strip():
            raise ValueError("Mã thiết bị không được để trống.")
        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")

        current_year = datetime.now().year
        if year_of_usage > current_year:
            raise ValueError(
                f"Năm sử dụng ({year_of_usage}) không được lớn hơn năm hiện tại ({current_year})."
            )

        self._device_id = device_id.strip()
        self.device_name = device_name.strip()
        self._year_of_usage = year_of_usage
        self._purchase_price = purchase_price
        self.status = status

    @property
    def device_id(self) -> str:
        """Mã thiết bị chỉ đọc, không cho phép thay đổi sau khi khởi tạo."""
        return self._device_id

    @property
    def year_of_usage(self) -> int:
        return self._year_of_usage

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @abstractmethod
    def calculate_annual_maintenance_cost(self) -> float:
        """Phương thức trừu tượng tính chi phí bảo trì dự kiến trong một năm."""
        pass

    def __str__(self) -> str:
        return (
            f"[{self.device_id}] {self.device_name} | Năm SD: {self.year_of_usage} "
            f"| Giá: {self.purchase_price:,.0f} VND | Trạng thái: {self.status.value}"
        )
    class TeachingDevice(Device):
     """Lớp trừu tượng cho thiết bị giảng dạy, bổ sung số ngày mượn tối đa."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        year_of_usage: int,
        purchase_price: float,
        max_borrow_days: int = 1,
        status: DeviceStatus = DeviceStatus.Available,
    ):
        super().__init__(device_id, device_name, year_of_usage, purchase_price, status)
        if max_borrow_days <= 0:
            raise ValueError("Số ngày mượn tối đa phải lớn hơn 0.")
        self.max_borrow_days = max_borrow_days

    def mark_as_borrowed(self) -> None:
        self.status = DeviceStatus.Borrowed

    def mark_as_available(self) -> None:
        self.status = DeviceStatus.Available

    def set_maintenance(self) -> None:
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
            device_id, device_name, year_of_usage, purchase_price, max_borrow_days=1, status=status
        )

    def calculate_annual_maintenance_cost(self) -> float:
        # 5% giá mua + 50.000 VNĐ phí pin
        return (self.purchase_price * 0.05) + 50_000.0


class Microphone(TeachingDevice):
    """Micro giảng dạy (hỗ trợ phân loại có dây / không dây)."""

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
            device_id, device_name, year_of_usage, purchase_price, max_borrow_days=1, status=status
        )
        self.is_wireless = is_wireless

    def calculate_annual_maintenance_cost(self) -> float:
        cost = self.purchase_price * 0.08
        if self.is_wireless:
            cost += 100_000.0  # Chi phí bảo dưỡng đầu thu không dây
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
            device_id, device_name, year_of_usage, purchase_price, max_borrow_days=1, status=status
        )

    def calculate_annual_maintenance_cost(self) -> float:
        return self.purchase_price * 0.04