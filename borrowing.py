
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
    DeviceNotInSlipException,
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
        if not isinstance(borrower_id, str) or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")

        if not isinstance(full_name, str) or not full_name.strip():
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
        if not isinstance(borrower_id, str) or not borrower_id.strip():
            raise ValueError("Mã người mượn không được để trống.")

        if not isinstance(full_name, str) or not full_name.strip():
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
        return 2


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

        if (
            not isinstance(from_period, int)
            or isinstance(from_period, bool)
            or not isinstance(to_period, int)
            or isinstance(to_period, bool)
            or from_period <= 0
            or to_period <= 0
        ):
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
        """Đánh dấu thiết bị đã được trả."""

        if self.is_returned:
            raise DeviceAlreadyReturnedException(
                self.device.device_id
            )

        if not isinstance(returned_date, datetime):
            raise TypeError("Ngày trả phải là đối tượng datetime.")

        if returned_date < self.borrowed_date:
            raise ValueError(
                "Ngày trả không được trước ngày mượn."
            )

        self.returned_date = returned_date
        self.device.mark_as_available()


class BorrowingSlip:
    """Phiếu mượn quản lý người mượn và các mục thiết bị."""

    LATE_FEE_PER_DAY = 20_000.0

    def __init__(
        self,
        slip_id: str,
        borrower: IBorrower,
        teaching_room: str,
        borrowed_date: datetime,
    ):
        if not isinstance(slip_id, str) or not slip_id.strip():
            raise ValueError("Mã phiếu mượn không hợp lệ.")

        if borrower is None:
            raise ValueError("Người mượn không hợp lệ.")

        if not isinstance(teaching_room, str) or not teaching_room.strip():
            raise ValueError("Phòng giảng dạy không hợp lệ.")

        if not isinstance(borrowed_date, datetime):
            raise TypeError("Ngày mượn phải là đối tượng datetime.")

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
        """Kiểm tra các điều kiện trước khi cho mượn thiết bị."""

        if device is None:
            raise ValueError("Thiết bị không được để trống.")

        if not isinstance(device, TeachingDevice):
            raise TypeError("Đối tượng phải là thiết bị giảng dạy.")

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

        # Không cho mượn cùng một thiết bị hai lần trên một phiếu.
        for item in self._items:
            if item.device.device_id.lower() == device.device_id.lower():
                raise DuplicateDeviceException(device.device_id)

        # Kiểm tra giới hạn số thiết bị của người mượn.
        if len(self._items) >= self.borrower.get_maximum_devices():
            raise BorrowLimitExceededException(
                self.borrower.borrower_id,
                self.borrower.get_maximum_devices(),
            )

        # Chỉ cho mượn thiết bị đang sẵn sàng.
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
        """Thêm thiết bị vào phiếu mượn."""

        # Bước 1: kiểm tra điều kiện.
        self._validate_borrowing(device, borrow_days)

        # Bước 2: xác định ngày đến hạn.
        due_date = self.borrowed_date + timedelta(days=borrow_days)

        # Bước 3: tạo mục mượn.
        item = BorrowItem(
            device=device,
            borrowed_date=self.borrowed_date,
            due_date=due_date,
        )

        # Bước 4: cập nhật trạng thái và lưu mục mượn.
        device.mark_as_borrowed()
        self._items.append(item)

    def return_device(
        self,
        device_id: str,
        returned_date: datetime,
    ) -> float:
        """Trả thiết bị và tính phí phạt trễ hạn."""

        if not isinstance(device_id, str) or not device_id.strip():
            raise ValueError("Mã thiết bị không hợp lệ.")

        if not isinstance(returned_date, datetime):
            raise TypeError("Ngày trả phải là đối tượng datetime.")

        target = device_id.strip().lower()

        # Tìm thiết bị trong phiếu mượn.
        item = next(
            (
                current_item
                for current_item in self._items
                if current_item.device.device_id.lower() == target
            ),
            None,
        )

        if item is None:
            raise DeviceNotInSlipException(device_id)

        if item.is_returned:
            raise DeviceAlreadyReturnedException(device_id)

        if returned_date < item.borrowed_date:
            raise ValueError("Ngày trả không được trước ngày mượn.")

        # Tính phí trước khi cập nhật trạng thái trả thiết bị.
        late_fee = 0.0

        if returned_date.date() > item.due_date.date():
            overdue_days = (
                returned_date.date() - item.due_date.date()
            ).days
            late_fee = overdue_days * self.LATE_FEE_PER_DAY

        # Xác nhận trả thiết bị.
        item.return_device(returned_date)

        return late_fee

    def calculate_total_late_fee(self) -> float:
        """Tính tổng phí phạt của các thiết bị đã trả trễ."""

        total = 0.0

        for item in self._items:
            if (
                item.is_returned
                and item.returned_date is not None
                and item.returned_date.date() > item.due_date.date()
            ):
                overdue_days = (
                    item.returned_date.date() - item.due_date.date()
                ).days

                total += overdue_days * self.LATE_FEE_PER_DAY

        return total

    def __str__(self) -> str:
        return (
            f"Phiếu mượn: {self.slip_id} "
            f"| Người mượn: {self.borrower.full_name} "
            f"| Mã người mượn: {self.borrower.borrower_id} "
            f"| Phòng: {self.teaching_room} "
            f"| Số thiết bị: {len(self._items)}"
        )
