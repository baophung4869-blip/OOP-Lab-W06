
"""
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

from devices import TeachingDevice, DeviceStatus
from exceptions import (
    BorrowLimitExceededException,
    DeviceAlreadyReturnedException,
    InvalidBorrowPeriodException,
    DuplicateDeviceException,
    DeviceUnavailableException,
)


class IBorrower(ABC):
    """Interface quy định hợp đồng cho đối tượng mượn thiết bị."""

    @property
    @abstractmethod
    def borrower_id(self) -> str:
        pass

    @property
    @abstractmethod
    def full_name(self) -> str:
        pass

    @abstractmethod
    def get_maximum_devices(self) -> int:
        pass


class Lecturer(IBorrower):
    """Giảng viên được mượn tối đa 3 thiết bị trên một phiếu."""

    def __init__(self, borrower_id: str, full_name: str):
        if not borrower_id or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")
        if not full_name or not full_name.strip():
            raise ValueError("Họ tên không được để trống.")

        self._borrower_id = borrower_id.strip()
        self._full_name = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:
        return 3


class TeachingAssistant(IBorrower):
    """Trợ giảng được mượn tối đa 2 thiết bị trên một phiếu."""

    def __init__(self, borrower_id: str, full_name: str):
        if not borrower_id or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")
        if not full_name or not full_name.strip():
            raise ValueError("Họ tên không được để trống.")

        self._borrower_id = borrower_id.strip()
        self._full_name = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:        return 2


class BorrowItem:
    """Chi tiết một thiết bị trong phiếu mượn."""

    def __init__(
        self,
        device: TeachingDevice,
        borrowed_date: datetime,
        due_date: datetime,
        from_period: int = 1,
        to_period: int = 3,
    ):
        if device is None:
            raise ValueError("Thiết bị không được để trống.")

        if due_date < borrowed_date:
            raise ValueError(
                "Ngày đến hạn phải sau hoặc bằng ngày mượn."
            )

        if from_period <= 0 or to_period <= 0:
            raise ValueError("Tiết học phải là số nguyên dương.")

        if to_period < from_period:
            raise ValueError(
                "Tiết kết thúc phải lớn hơn hoặc bằng tiết bắt đầu."
            )

        self.device = device
        self.borrowed_date = borrowed_date
        self.due_date = due_date
        self.from_period = from_period
        self.to_period = to_period
        self.returned_date: Optional[datetime] = None

    @property
    def is_returned(self) -> bool:
        return self.returned_date is not None

    def return_device(self, returned_date: datetime) -> None:
        if self.is_returned:
            raise DeviceAlreadyReturnedException(
                self.device.device_id
            )

        if returned_date < self.borrowed_date:
            raise ValueError(
                "Ngày trả không được trước ngày mượn."
            )

        self.returned_date = returned_date
        self.device.mark_as_available()


class BorrowingSlip:
    """Phiếu mượn quản lý người mượn và các mục thiết bị."""

    def __init__(
        self,
        slip_id: str,
        borrower: IBorrower,
        teaching_room: str,
        borrowed_date: datetime,
    ):
        if not slip_id or not slip_id.strip():
            raise ValueError("Mã phiếu mượn không hợp lệ.")

        if borrower is None:
            raise ValueError("Người mượn không hợp lệ.")

        if not teaching_room or not teaching_room.strip():
            raise ValueError("Phòng giảng dạy không hợp lệ.")

        self.slip_id = slip_id.strip()
        self.borrower = borrower
        self.teaching_room = teaching_room.strip()
        self.borrowed_date = borrowed_date
        self._items: List[BorrowItem] = []

    @property
    def items(self) -> List[BorrowItem]:
        """Trả về bản sao danh sách mục mượn."""
        return self._items.copy()

    def _validate_borrowing(
        self,
        device: TeachingDevice,
        borrow_days: int,
    ) -> None:
        """Kiểm tra điều kiện trước khi thay đổi trạng thái thiết bị."""

        if device is None:
            raise ValueError("Thiết bị không được để trống.")

        if (
            not isinstance(borrow_days, int)
            or isinstance(borrow_days, bool)
            or borrow_days <= 0
            or borrow_days > device.max_borrow_days
        ):
            raise InvalidBorrowPeriodException(
                device.device_id,
                borrow_days,
                device.max_borrow_days,
            )

        if any(
            item.device.device_id.lower()
            == device.device_id.lower()
            for item in self._items
        ):
            raise DuplicateDeviceException(device.device_id)

        if len(self._items) >= self.borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self.borrower.borrower_id,
                self.borrower.get_maximum_devices(),
            )

        if device.status != DeviceStatus.Available:
            raise DeviceUnavailableException(
                device.device_id,
                device.status,
            )

    def add_device(
        self,
        device: TeachingDevice,
        borrow_days: int,
    ) -> None:
        """Thêm thiết bị sau khi xác thực toàn bộ điều kiện."""

        # Bước 1: xác thực trước.
        self._validate_borrowing(device, borrow_days)

        # Bước 2: tạo mục mượn sau khi xác thực thành công.
        due_date = self.borrowed_date + timedelta(days=borrow_days)

        item = BorrowItem(
            device=device,
            borrowed_date=self.borrowed_date,
            due_date=due_date,
        )

        # Bước 3: cập nhật trạng thái và lưu mục mượn.
        device.mark_as_borrowed()
        self._items.append(item)
