import os
from unittest import mock

import geopandas
import pandas as pd

from project.CrimeDataTransformation import CrimeDataCleaner
from project.La311DataTransformation import La311Cleaner
from project.pipeline import Pipeline


#
def test_system_pipeline_mock():
    """
    System-Test, Validates that the output file(s) exist, extraction mocked
    Note: See below for test_system_pipeline_with_extract that also includes the extraction process
    :return:
    """
    pipeline = init_pipeline()
    mock_crime_data(pipeline.crime_data_transformation)
    mock_la311(pipeline.la311_data_transformation)

    with mock.patch.object(pipeline, 'extract') as mock_extract:
        output_path = pipeline.run_pipeline()
        assert (mock_extract.call_count, 1)
        assert os.path.exists(output_path)


def test_extract():
    pipeline = init_pipeline()
    pipeline.extract()
    assert os.path.exists(pipeline.crime_data_path), "Could not find file with Crime Data"
    assert os.path.exists(pipeline.la311_data_path), "Could not find file with LA311 Data"
    assert os.path.exists(pipeline.zip_data_path), "Could not find file with ZIP regions Data"
    assert os.path.exists(pipeline.street_data_path), "Could not find file with Street Name Data"


def test_transform_crime_data():
    total_invalid_threshold = 0.1
    crime_data_transform = CrimeDataCleaner(total_invalid_threshold)
    mock_crime_data(crime_data_transform)
    crime_data_transform.transform_crimedata()
    print(crime_data_transform.data.shape)
    assert (crime_data_transform.data.shape, (2, 21)), "Rows/ columns missing!"
    assert (len(crime_data_transform.data[crime_data_transform.data["Zipcode"].isna()]), 0), "ZIP Codes missing"


def test_transform_la311_data():
    total_invalid_threshold = 0.1
    la311_data_transform = La311Cleaner(total_invalid_threshold)
    mock_la311(la311_data_transform)
    la311_data_transform.transform_data()
    assert (la311_data_transform.data.shape, (2, 35))


def test_load():
    pipeline = init_pipeline()
    mock_crime_data(pipeline.crime_data_transformation)
    mock_la311(pipeline.la311_data_transformation)

    pipeline.transform()
    with mock.patch.object(pipeline.data_loader, 'load_data') as mock_load:
        pipeline.load()
        assert (mock_load.call_count, 2)


def test_system_pipeline_with_extract():
    """
    Tests complete Pipeline, including data fetch from external sources.
    NOTE: It's suggested to run tests to be independently of external resources,
    so running test_system_pipeline_mock is preferred
    :param self:
    :return:
    """
    print("running pipeline test")
    total_invalid_threshold = 0.1
    download_timeout_seconds = 500

    pipeline = Pipeline(total_invalid_threshold, download_timeout_seconds)
    output_path = pipeline.run_pipeline()
    assert os.path.exists(output_path)


# Helper Functions that are reused #
def mock_la311(transform):
    la311_mock_data = pd.read_csv('test_data/la311_test_data.csv')
    transform.data = la311_mock_data


def mock_crime_data(transform):
    crime_mock_data = pd.read_csv('test_data/crime_test_data.csv')
    street_mock_data = pd.read_csv('test_data/street_test_data.csv', usecols=["Street Name", "Street Suffix"])
    zip_mock_data = geopandas.read_file('test_data/shapefile_test_data/zip_test_data.shp')

    transform.data = crime_mock_data
    transform.street_data = street_mock_data
    transform.zip_data = zip_mock_data


def init_pipeline():
    total_invalid_threshold = 0.1
    download_timeout_seconds = 500
    pipeline = Pipeline(total_invalid_threshold, download_timeout_seconds)
    return pipeline
