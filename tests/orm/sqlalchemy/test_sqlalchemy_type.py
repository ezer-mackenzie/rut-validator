import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from rut_validator.core.orm.sqlalchemy.schema import RutSQLAlchemy

Base = declarative_base()

class TestModel(Base):
    __tablename__ = 'test_model'
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