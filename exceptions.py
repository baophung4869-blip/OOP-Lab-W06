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