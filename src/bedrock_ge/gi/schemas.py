"""pandera schemas for Bedrock GI data. Base schemas refer to schemas that have no calculated GIS geometry or values."""

from typing import Optional

import pandera.pandas as pa
from pandera.typing import Series
from pandera.typing.geopandas import GeoSeries


class Project(pa.DataFrameModel):
    project_uid: Series[str] = pa.Field(
        # primary_key=True,
        unique=True,
    )
    crs_wkt: Series[str] = pa.Field(description="Coordinate Reference System")
    # datum: Series[str] = pa.Field(description="Datum used for measurement of the ground level elevation.")


class BaseLocation(pa.DataFrameModel):
    location_uid: Series[str] = pa.Field(
        # primary_key=True,
        unique=True,
    )
    project_uid: Series[str] = pa.Field(
        # foreign_key="project.project_uid"
    )
    location_source_id: Series[str]
    location_type: Series[str]
    easting: Series[float] = pa.Field(coerce=True)
    northing: Series[float] = pa.Field(coerce=True)
    ground_level_elevation: Series[float] = pa.Field(
        coerce=True,
        description="Elevation w.r.t. a local datum. Usually the orthometric height from the geoid, i.e. mean sea level, to the ground level.",
    )
    depth_to_base: Series[float]


class Location(BaseLocation):
    elevation_at_base: Series[float]
    longitude: Series[float]
    latitude: Series[float]
    wgs84_ground_level_height: Series[float] = pa.Field(
        description="Ground level height w.r.t. the WGS84 (World Geodetic System 1984) ellipsoid.",
        nullable=True,
    )
    geometry: GeoSeries


class BaseInSitu(pa.DataFrameModel):
    project_uid: Series[str] = pa.Field(
        # foreign_key="project.project_uid"
    )
    location_uid: Series[str] = pa.Field(
        # foreign_key="location.location_uid"
    )
    depth_to_top: Series[float] = pa.Field(coerce=True)
    depth_to_base: Optional[Series[float]] = pa.Field(coerce=True, nullable=True)


class BaseSample(BaseInSitu):
    sample_uid: Series[str] = pa.Field(
        # primary_key=True,
        unique=True,
    )
    sample_source_id: Series[str]


class Sample(BaseSample):
    elevation_at_top: Series[float]
    elevation_at_base: Optional[Series[float]] = pa.Field(nullable=True)
    geometry: GeoSeries


class InSitu(BaseInSitu):
    elevation_at_top: Series[float]
    elevation_at_base: Optional[Series[float]] = pa.Field(nullable=True)
    geometry: GeoSeries


class BaseLab(pa.DataFrameModel):
    project_uid: Series[str] = pa.Field(
        # foreign_key="project.project_uid"
    )
    location_uid: Series[str] = pa.Field(
        # foreign_key="location.location_uid"
    )
    sample_uid: Series[str] = pa.Field(
        # foreign_key="sample.sample_uid"
    )


class Lab(BaseLab):
    geometry: GeoSeries = pa.Field(
        description="GIS geometry of the sample on which this lab test was performed."
    )
