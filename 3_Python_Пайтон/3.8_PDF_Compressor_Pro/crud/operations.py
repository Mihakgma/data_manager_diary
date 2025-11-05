from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.models import (
    ProcessedFile, Setting, FailReason,
    NestingDepth, CompressionMethod
)
from typing import Optional, List
import datetime


class DBOperations:
    def __init__(self, db: Session):
        self.db = db

    # Операции с ProcessedFile
    def get_processed_file_by_path(self, file_path: str) -> Optional[ProcessedFile]:
        return self.db.query(ProcessedFile).filter(
            ProcessedFile.file_full_path == file_path
        ).first()

    def create_processed_file(
            self,
            file_full_path: str,
            is_successful: bool,
            setting_id: int,
            file_compression_kbites: float = 0.0,
            fail_reason_id: Optional[int] = None,
            other_fail_reason: Optional[str] = None
    ) -> ProcessedFile:
        processed_file = ProcessedFile(
            file_full_path=file_full_path,
            is_successful=is_successful,
            fail_reason_id=fail_reason_id,
            setting_id=setting_id,
            file_compression_kbites=file_compression_kbites,
            other_fail_reason=other_fail_reason
        )
        self.db.add(processed_file)
        self.db.commit()
        self.db.refresh(processed_file)
        return processed_file

    # Операции с Setting
    def get_active_setting(self) -> Optional[Setting]:
        return self.db.query(Setting).filter(Setting.is_active == True).first()

    def find_existing_setting(
            self,
            nesting_depth_id: int,
            need_replace: bool,
            compression_level: int,
            compression_method_id: int,
            compression_min_boundary: int,
            procession_timeout: int
    ) -> Optional[Setting]:
        """Находит существующую настройку с такими же параметрами"""
        return self.db.query(Setting).filter(
            and_(
                Setting.nesting_depth_id == nesting_depth_id,
                Setting.need_replace == need_replace,
                Setting.compression_level == compression_level,
                Setting.compression_method_id == compression_method_id,
                Setting.compression_min_boundary == compression_min_boundary,
                Setting.procession_timeout == procession_timeout
            )
        ).first()

    def create_setting(
            self,
            nesting_depth_id: int,
            need_replace: bool = True,
            compression_level: int = 2,
            compression_method_id: int = 1,
            compression_min_boundary: int = 1024,
            procession_timeout: int = 35,
            info: Optional[str] = None,
            activate: bool = True
    ) -> Setting:
        # Сначала проверяем, существует ли уже такая настройка
        existing_setting = self.find_existing_setting(
            nesting_depth_id=nesting_depth_id,
            need_replace=need_replace,
            compression_level=compression_level,
            compression_method_id=compression_method_id,
            compression_min_boundary=compression_min_boundary,
            procession_timeout=procession_timeout
        )

        if existing_setting:
            # Если настройка уже существует, просто активируем ее
            if activate:
                return self.activate_setting(existing_setting.id)
            return existing_setting

        # Если настройки не существует, создаем новую
        if activate:
            # Деактивируем все текущие настройки
            self.db.query(Setting).update({Setting.is_active: False})
            self.db.commit()

        setting = Setting(
            nesting_depth_id=nesting_depth_id,
            need_replace=need_replace,
            compression_level=compression_level,
            compression_method_id=compression_method_id,
            compression_min_boundary=compression_min_boundary,
            procession_timeout=procession_timeout,
            is_active=activate,
            info=info or f"Создано {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

        self.db.add(setting)
        self.db.commit()
        self.db.refresh(setting)
        return setting

    def activate_setting(self, setting_id: int) -> Setting:
        # Деактивируем все настройки
        self.db.query(Setting).update({Setting.is_active: False})

        # Активируем выбранную
        setting = self.db.query(Setting).filter(Setting.id == setting_id).first()
        if setting:
            setting.is_active = True
            self.db.commit()
            self.db.refresh(setting)
        return setting

    def get_all_settings(self) -> List[Setting]:
        return self.db.query(Setting).order_by(Setting.created_at.desc()).all()

    def update_setting_info(self, setting_id: int, info: str) -> Setting:
        setting = self.db.query(Setting).filter(Setting.id == setting_id).first()
        if setting:
            setting.info = info
            self.db.commit()
            self.db.refresh(setting)
        return setting

    # Операции с FailReason
    def get_fail_reason_by_name(self, name: str) -> Optional[FailReason]:
        return self.db.query(FailReason).filter(FailReason.name == name).first()

    def get_all_fail_reasons(self) -> List[FailReason]:
        return self.db.query(FailReason).all()

    def update_fail_reason_info(self, fail_reason_id: int, info: str) -> FailReason:
        fail_reason = self.db.query(FailReason).filter(FailReason.id == fail_reason_id).first()
        if fail_reason:
            fail_reason.info = info
            self.db.commit()
            self.db.refresh(fail_reason)
        return fail_reason

    # Операции с CompressionMethod
    def get_compression_method_by_name(self, name: str) -> Optional[CompressionMethod]:
        return self.db.query(CompressionMethod).filter(CompressionMethod.name == name).first()

    def get_all_compression_methods(self) -> List[CompressionMethod]:
        return self.db.query(CompressionMethod).all()

    # Инициализация базовых данных
    def initialize_base_data(self):
        # Создаем причины ошибок
        fail_reasons = [
            {"name": "размер увеличился при сжатии",
             "info": "Файл был пропущен, так как размер после сжатия увеличился"},
            {"name": "превышен таймаут обработки файла",
             "info": "Обработка файла заняла больше времени, чем установленный таймаут"},
            {"name": "прочая причина", "info": "Другие причины ошибок при обработке файла"}
        ]

        for reason_data in fail_reasons:
            if not self.get_fail_reason_by_name(reason_data["name"]):
                fail_reason = FailReason(**reason_data)
                self.db.add(fail_reason)

        # Создаем методы глубины вложенности
        depth_names = ["Только текущая", "1 уровень", "2 уровня", "Все поддиректории"]
        for i, name in enumerate(depth_names, 1):
            if not self.db.query(NestingDepth).filter(NestingDepth.name == name).first():
                depth = NestingDepth(id=i, name=name)
                self.db.add(depth)

        # Создаем методы сжатия
        method_names = ["Ghostscript", "Стандартное", "Только изображения"]
        for i, name in enumerate(method_names, 1):
            if not self.db.query(CompressionMethod).filter(CompressionMethod.name == name).first():
                method = CompressionMethod(name=name)
                self.db.add(method)

        self.db.commit()

        # Создаем настройку по умолчанию, если нет активных
        if not self.get_active_setting():
            self.create_setting(
                nesting_depth_id=4,  # Все поддиректории
                need_replace=True,
                compression_level=2,
                compression_method_id=1,  # Ghostscript
                compression_min_boundary=1024,
                procession_timeout=35,
                info="Настройка по умолчанию",
                activate=True
            )
