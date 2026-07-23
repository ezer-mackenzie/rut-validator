import pytest
from sqlalchemy import Column, Integer, create_engine, select
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session, declarative_base

from rut_validator.orm.sqlalchemy import RutSQLAlchemy

Base = declarative_base()


class TestModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    rut = Column(RutSQLAlchemy)


def test_valid_rut_processes_bind_param():
    type_instance = RutSQLAlchemy()
    processed = type_instance.process_bind_param("12.345.678-5", None)
    assert processed == "123456785"


def test_invalid_rut_raises_value_error_on_bind():
    type_instance = RutSQLAlchemy()
    with pytest.raises(ValueError):
        type_instance.process_bind_param("invalid-rut", None)


def test_none_bind_param_returns_none():
    type_instance = RutSQLAlchemy()
    assert type_instance.process_bind_param(None, None) is None


def test_result_value_returns_stored_string():
    type_instance = RutSQLAlchemy()
    result = type_instance.process_result_value("123456785", None)
    assert result == "123456785"


def test_sqlalchemy_session_round_trip_normalizes_value():
    engine = create_engine("sqlite://")
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            session.add(TestModel(rut="12.345.678-5"))
            session.commit()
            stored = session.scalars(select(TestModel)).one()
            assert stored.rut == "123456785"
    finally:
        engine.dispose()


def test_sqlalchemy_session_rejects_invalid_value():
    engine = create_engine("sqlite://")
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            session.add(TestModel(rut="invalid"))
            with pytest.raises(StatementError):
                session.commit()
    finally:
        engine.dispose()
