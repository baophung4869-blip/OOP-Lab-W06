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