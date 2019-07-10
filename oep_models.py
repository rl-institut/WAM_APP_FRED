# Add all open_FRED table models form source DB: OEP
# pylint: disable=redefined-outer-name

from sqlalchemy import (
    BigInteger as BI,
    Column as C,
    DateTime as DT,
    Float,
    ForeignKey as FK,
    Integer as Int,
    Interval,
    JSON,
    MetaData,
    String as Str,
    Text,
    UniqueConstraint as UC,
    Table,
    Numeric)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlahelper as sah
from geoalchemy2 import types as geotypes

# import WAM_APP_FRED.app_settings
# from geoalchemy2.types import Geometry
# from WAM_APP_FRED.cli.openFRED import mapped_classes, db_session


# ##########################################SQLAlchemy setup########################################
SCHEMA_1 = 'model_draft'
SCHEMA_2 = 'supply'
engine = sah.get_engine('oep_engine')
metadata_1 = MetaData(schema=SCHEMA_1, bind=engine)
metadata_2 = MetaData(schema=SCHEMA_2, bind=engine)
# ##########################################TABLE DEFINITION########################################

# included function from github: https://github.com/open-fred/cli/blob/master/openFRED.py
# copied function to avoid dependencies


def mapped_classes(metadata):
    """ Returns classes mapped to the openFRED database via SQLAlchemy.
    The classes are dynamically created and stored in a dictionary keyed by
    class names. The dictionary also contains the special entry `__Base__`,
    which an SQLAlchemy `declarative_base` instance used as the base class from
    which all mapped classes inherit.
    """

    Base = declarative_base(metadata=metadata)
    classes = {"__Base__": Base}

    def map(name, registry, namespace):
        namespace["__tablename__"] = "openfred_" + name.lower()
        namespace["__table_args__"] = namespace.get("__table_args__", ()) + (
            {"keep_existing": True},
        )
        if namespace["__tablename__"][-1] != "s":
            namespace["__tablename__"] += "s"
        registry[name] = type(name, (registry["__Base__"],), namespace)

    map(
        "Timespan",
        classes,
        {
            "id": C(BI, primary_key=True),
            "start": C(DT),
            "stop": C(DT),
            "resolution": C(Interval),
            "segments": C(ARRAY(DT, dimensions=2)),
            "__table_args__": (UC("start", "stop", "resolution"),),
        },
    )
    map(
        "Location",
        classes,
        {
            "id": C(BI, primary_key=True),
            "point": C(
                geotypes.Geometry(geometry_type="POINT", srid=4326),
                unique=True,
            ),
        },
    )
    # TODO: Handle units.

    class Variable(Base):
        __table_args__ = ({"keep_existing": True},)
        __tablename__ = "openfred_variables"
        id = C(BI, primary_key=True)
        name = C(Str(255), nullable=False, unique=True)
        # TODO: Figure out whether and where this is in the '.nc' files.
        type = C(Str(37))
        netcdf_attributes = C(JSON)
        description = C(Text)
        standard_name = C(Str(255))
        __mapper_args_ = {
            "polymorphic_identity": "variable",
            "polymorphic_on": type,
        }

    classes["Variable"] = Variable

    class Flags(Variable):
        __table_args__ = ({"keep_existing": True},)
        __tablename__ = "openfred_flags"
        id = C(BI, FK(Variable.id), primary_key=True)
        flag_ks = C(ARRAY(Int), nullable=False)
        flag_vs = C(ARRAY(Str(37)), nullable=False)
        __mapper_args_ = {"polymorphic_identity": "flags"}

        @property
        def flag(self, key):
            flags = dict(zip(self.flag_ks, self.flag_vs))
            return flags[key]

    classes["Flags"] = Flags

    class Series(Base):
        __tablename__ = "openfred_series"
        __table_args__ = (
            UC("height", "location_id", "timespan_id", "variable_id"),
            {"keep_existing": True},
        )
        id = C(BI, primary_key=True)
        values = C(ARRAY(Float), nullable=False)
        height = C(Float)
        timespan_id = C(BI, FK(classes["Timespan"].id), nullable=False)
        location_id = C(BI, FK(classes["Location"].id), nullable=False)
        variable_id = C(BI, FK(classes["Variable"].id), nullable=False)
        timespan = relationship(classes["Timespan"], backref="series")
        location = relationship(classes["Location"], backref="series")
        variable = relationship(classes["Variable"], backref="series")

    classes["Series"] = Series

    return classes


def ppr_mapping(metadata):
    """
    Returns classes mapped to the OEDB database via SQLAlchemy.
    The classes are reflected(autoload=True) and stored in a dictionary keyed by
    class names. The dictionary also contains the special entry `__Base__`,
    which an SQLAlchemy `declarative_base` instance used as the base class from
    which all mapped classes inherit.
    """

    # SQLAlchemy Base
    Base = declarative_base(metadata=metadata)
    classes = {"__Base__": Base}

    # Table definition with MetaData object
    class ResPowerPlantRegister(Base):
        __table__ = Table('ego_dp_res_powerplant', metadata)
        # reflect the existing table with autoload from DB and add values as extend_existing
        Table('ego_dp_res_powerplant', metadata, extend_existing=True, autoload=True)

        # Convert the type Decimal into float for python
        for column in __table__.columns.values():
            if isinstance(column.type, Numeric):
                column.type.asdecimal = False

    # Add Table to dict
    classes["ResPowerPlant"] = ResPowerPlantRegister
    return classes


# contains open_FRED related tables as SQLAlchemy class
open_fred_classes = mapped_classes(metadata_1)
ego_dp_res_classes = ppr_mapping(metadata_2)
