"""
/****************/
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
/****************/
"""
from abc import ABC, abstractmethod


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
    """Giảng viên: Được mượn tối đa 3 thiết bị trên một phiếu."""

    def __init__(self, borrower_id: str, full_name: str):
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
    """Trợ giảng: Được mượn tối đa 2 thiết bị trên một phiếu."""

    def __init__(self, borrower_id: str, full_name: str):
        self._borrower_id = borrower_id.strip()
        self._full_name = full_name.strip()

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:
        return 2
from datetime import datetime, timedelta
from typing import List, Optional
from devices import TeachingDevice
from exceptions import (
    BorrowLimitExceededException,
    DeviceAlreadyReturnedException,
)


class BorrowItem:
    """Chi tiết một mục thiết bị trong phiếu mượn."""

    def __init__(
        self,
        device: TeachingDevice,
        borrowed_date: datetime,
        due_date: datetime,
        from_period: int = 1,
        to_period: int = 3,
    ):
        if device is None:
            raise ValueError("Device không được null[cite: 3].")
        if due_date < borrowed_date:
            raise ValueError("DueDate phải sau hoặc bằng BorrowedDate[cite: 3].")
        if to_period < from_period:
            raise ValueError("Tiết kết thúc phải lớn hơn hoặc bằng tiết bắt đầu.")

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
            raise DeviceAlreadyReturnedException(self.device.device_id)
        if returned_date < self.borrowed_date:
            raise ValueError("Ngày trả không được trước ngày mượn[cite: 3, 4].")

        self.returned_date = returned_date
        self.device.mark_as_available()


class BorrowingSlip:
    """Phiếu mượn thiết bị hợp thành các BorrowItem[cite: 4]."""

    def __init__(
        self,
        slip_id: str,
        borrower: IBorrower,
        teaching_room: str,
        borrowed_date: datetime,
    ):
        if not slip_id or not slip_id.strip():
            raise ValueError("SlipId không hợp lệ.")
        if borrower is None:
            raise ValueError("Borrower không hợp lệ.")
        if not teaching_room or not teaching_room.strip():
            raise ValueError("TeachingRoom không hợp lệ.")

        self.slip_id = slip_id.strip()
        self.borrower = borrower
        self.teaching_room = teaching_room.strip()
        self.borrowed_date = borrowed_date
        self._items: List[BorrowItem] = []

    @property
    def items(self) -> List[BorrowItem]:
        return list(self._items)

    def add_device(self, device: TeachingDevice, borrow_days: int) -> None:
        # Phiên bản sơ khởi chưa tối ưu thứ tự kiểm tra (sẽ refactor/fix ở bước 10)
        device.mark_as_borrowed()
        if len(self._items) >= self.borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self.borrower.borrower_id, self.borrower.get_maximum_devices()
            )
        item = BorrowItem(
            device,
            self.borrowed_date,
            self.borrowed_date + timedelta(days=borrow_days),
        )
        self._items.append(item)