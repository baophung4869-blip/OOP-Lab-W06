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