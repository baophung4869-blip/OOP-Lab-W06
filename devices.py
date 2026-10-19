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
class ClassRoom:
    """Lớp phòng học, thực hiện kết tập danh sách thiết bị."""

    def __init__(self, room_id: str, room_name: str, capacity: int):
        if not room_id or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")
        if capacity <= 0:
            raise ValueError("Sức chứa phòng phải lớn hơn 0.")

        self.room_id = room_id.strip()
        self.room_name = room_name.strip()
        self.capacity = capacity
        self._devices: List[Device] = []

    @property
    def devices(self) -> List[Device]:
        return list(self._devices)

    def add_device(self, device: Device) -> bool:
        """Quy tắc 1 & 2: Không thêm thiết bị trùng mã hoặc null."""
        if device is None:
            raise ValueError("Không chấp nhận đối tượng thiết bị null.")
        if any(d.device_id.lower() == device.device_id.lower() for d in self._devices):
            return False
        self._devices.append(device)
        return True

    def remove_device(self, device_id: str) -> bool:
        dev = self.find_device(device_id)
        if dev:
            self._devices.remove(dev)
            return True
        return False

    def find_device(self, device_id: str) -> Optional[Device]:
        if not device_id or not device_id.strip():
            return None
        target = device_id.strip().lower()
        for d in self._devices:
            if d.device_id.lower() == target:
                return d
        return None

    def calculate_annual_maintenance_cost(self) -> float:
        """Quy tắc 3: Sử dụng tính đa hình hoàn toàn."""
        return sum(d.calculate_annual_maintenance_cost() for d in self._devices)

    def get_devices_requiring_maintenance(self) -> List[Device]:
        """Quy tắc 4: Lọc thiết bị cần bảo trì (UnderMaintenance hoặc dùng trên 5 năm)."""
        current_year = datetime.now().year
        return [
            d for d in self._devices
            if d.status == DeviceStatus.UnderMaintenance
            or (current_year - d.year_of_usage > 5)
        ]