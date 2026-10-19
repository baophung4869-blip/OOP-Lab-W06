"""
/****************/
Mã sinh viên: 20237303
Họ tên: Phùng Ngọc Bảo
/****************/
"""
from typing import Optional


class BorrowingException(Exception):
    """Ngoại lệ cơ sở cho toàn bộ nghiệp vụ mượn trả thiết bị."""

    def __init__(self, message: str, inner_exception: Optional[Exception] = None):
        super().__init__(message)
        self.inner_exception = inner_exception


class DeviceUnavailableException(BorrowingException):
    """Phát sinh khi thiết bị không ở trạng thái Available."""

    def __init__(self, device_id: str, current_status):
        self.device_id = device_id
        self.current_status = current_status
        super().__init__(
            f"Thiết bị '{device_id}' không ở trạng thái sẵn sàng (Trạng thái hiện tại: {current_status})."
        )


class BorrowLimitExceededException(BorrowingException):
    """Phát sinh khi người mượn đã đạt số thiết bị tối đa."""

    def __init__(self, borrower_id: str, maximum_devices: int):
        self.borrower_id = borrower_id
        self.maximum_devices = maximum_devices
        super().__init__(
            f"Người mượn '{borrower_id}' đã đạt giới hạn mượn tối đa ({maximum_devices} thiết bị)."
        )


class InvalidBorrowPeriodException(BorrowingException):
    """Phát sinh khi số ngày mượn không dương hoặc vượt quá giới hạn của thiết bị."""

    def __init__(self, device_id: str, requested_days: int, max_days: int):
        self.device_id = device_id
        self.requested_days = requested_days
        self.max_days = max_days
        super().__init__(
            f"Thời hạn mượn {requested_days} ngày không hợp lệ đối với thiết bị '{device_id}' (Giới hạn tối đa: {max_days} ngày)."
        )


class DuplicateDeviceException(BorrowingException):
    """Phát sinh khi cùng một thiết bị đã tồn tại trong phiếu."""

    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' đã tồn tại trong phiếu mượn.")


class DeviceNotInSlipException(BorrowingException):
    """Phát sinh khi yêu cầu trả một thiết bị không thuộc phiếu."""

    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' không thuộc phiếu mượn này.")


class DeviceAlreadyReturnedException(BorrowingException):
    """Phát sinh khi thiết bị trong phiếu đã được trả trước đó."""

    def __init__(self, device_id: str):
        self.device_id = device_id
        super().__init__(f"Thiết bị '{device_id}' trong phiếu đã được trả trước đó.")