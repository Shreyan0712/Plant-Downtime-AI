from typing import Optional
import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Machines(Base):
    __tablename__ = 'machines'
    __table_args__ = (
        PrimaryKeyConstraint('machine_id', name='machines_pkey'),
    )

    machine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    machine_name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100))
    category: Mapped[Optional[str]] = mapped_column(String(50))
    install_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(50))

    downtime_events: Mapped[list['DowntimeEvents']] = relationship('DowntimeEvents', back_populates='machine')
    maintenance_logs: Mapped[list['MaintenanceLogs']] = relationship('MaintenanceLogs', back_populates='machine')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        Index('ix_users_email', 'email', unique=True),
        Index('ix_users_id', 'id'),
        Index('ix_users_username', 'username', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DowntimeEvents(Base):
    __tablename__ = 'downtime_events'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['machines.machine_id'], name='fk_dt_machine'),
        PrimaryKeyConstraint('downtime_id', name='downtime_events_pkey')
    )

    downtime_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    machine_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    downtime_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    reason_category: Mapped[Optional[str]] = mapped_column(String(100))
    reason_details: Mapped[Optional[str]] = mapped_column(String(255))
    reported_by: Mapped[Optional[str]] = mapped_column(String(100))

    machine: Mapped['Machines'] = relationship('Machines', back_populates='downtime_events')
    downtime_causes: Mapped[list['DowntimeCauses']] = relationship('DowntimeCauses', back_populates='downtime')


class MaintenanceLogs(Base):
    __tablename__ = 'maintenance_logs'
    __table_args__ = (
        ForeignKeyConstraint(['machine_id'], ['machines.machine_id'], name='fk_maint_machine'),       
        PrimaryKeyConstraint('maintenance_id', name='maintenance_logs_pkey')
    )

    maintenance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    machine_id: Mapped[int] = mapped_column(Integer, nullable=False)
    maintenance_type: Mapped[Optional[str]] = mapped_column(String(50))
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    work_done: Mapped[Optional[str]] = mapped_column(Text)
    technician: Mapped[Optional[str]] = mapped_column(String(100))

    machine: Mapped['Machines'] = relationship('Machines', back_populates='maintenance_logs')


class DowntimeCauses(Base):
    __tablename__ = 'downtime_causes'
    __table_args__ = (
        ForeignKeyConstraint(['downtime_id'], ['downtime_events.downtime_id'], name='fk_dt_cause'),
        PrimaryKeyConstraint('cause_id', name='downtime_causes_pkey')
    )

    cause_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    downtime_id: Mapped[int] = mapped_column(Integer, nullable=False)
    root_cause: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    corrective_action: Mapped[Optional[str]] = mapped_column(Text)
    preventive_action: Mapped[Optional[str]] = mapped_column(Text)

    downtime: Mapped['DowntimeEvents'] = relationship('DowntimeEvents', back_populates='downtime_causes')