import pytest
from botocore.exceptions import ClientError

from src.exceptions import GetDataError
from src.utils.get_data import get_data


class TestGetData:
    def test_get_data_calls_get_file_type(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        mocker.patch("src.utils.get_data.handle_csv")

        get_file_type.return_value = "csv"
        get_data("s3://bucket/data/file.csv")

        get_file_type.assert_called_once_with("s3://bucket/data/file.csv")

    def test_get_data_calls_handle_csv_when_file_type_is_csv(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_csv = mocker.patch("src.utils.get_data.handle_csv")

        get_file_type.return_value = "csv"
        get_data("s3://bucket/data/file.csv")

        handle_csv.assert_called_once_with("bucket", "data/file.csv")

    def test_get_data_calls_handle_csv_when_file_type_is_json(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_json = mocker.patch("src.utils.get_data.handle_json")

        get_file_type.return_value = "json"
        get_data("s3://bucket/data/file.json")

        handle_json.assert_called_once_with("bucket", "data/file.json")

    def test_get_data_calls_handle_csv_when_file_type_is_parquet(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_parquet = mocker.patch("src.utils.get_data.handle_parquet")

        get_file_type.return_value = "parquet"
        get_data("s3://bucket/data/file.parquet")

        handle_parquet.assert_called_once_with("bucket", "data/file.parquet")

    def test_get_data_calls_handle_csv_when_file_type_is_xml(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_xml = mocker.patch("src.utils.get_data.handle_xml")

        get_file_type.return_value = "xml"
        get_data("s3://bucket/data/file.xml")

        handle_xml.assert_called_once_with("bucket", "data/file.xml")

    def test_get_data_calls_returns_expected_data(
        self, mocker, test_shallow_data
    ):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_csv = mocker.patch("src.utils.get_data.handle_csv")

        get_file_type.return_value = "csv"
        handle_csv.return_value = test_shallow_data["shallow_list_based"]

        result = get_data("s3://bucket/data/file.csv")

        assert result == test_shallow_data["shallow_list_based"]


@pytest.mark.error_handling
class TestGetDataErrorHandling:
    def test_get_data_handles_unsupported_file_type(self, mocker):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")

        get_file_type.return_value = "txt"

        with pytest.raises(TypeError) as e:
            get_data("s3://bucket/data/file.txt")

        assert str(e.value) == ("file type .txt is not supported")

    def test_raises_get_data_error_for_caught_exceptions(self, mocker, caplog):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        get_file_type.side_effect = Exception

        file_path = "s3://bucket/data/file.csv"
        with pytest.raises(GetDataError):
            get_data(file_path)


@pytest.mark.error_handling
class TestClientErrorResponses:
    @pytest.mark.parametrize(
        "file_path, exception",
        [
            ("s3://test-bucket/missing_file.csv", FileNotFoundError),
            ("s3://test-bucket/protected_file.csv", PermissionError),
            ("s3://test-bucket/other_file.csv", IOError),
            ("s3://test-bucket/invalid_data.csv", GetDataError),
        ],
    )
    def test_get_data_client_errors(self, mocker, file_path, exception):
        get_file_type = mocker.patch("src.utils.get_data.get_file_type")
        handle_csv = mocker.patch("src.utils.get_data.handle_csv")
        get_file_type.return_value = "csv"

        if exception == FileNotFoundError:
            handle_csv.side_effect = ClientError(
                {"Error": {"Code": "NoSuchKey"}}, "operation_name"
            )
        elif exception == PermissionError:
            handle_csv.side_effect = ClientError(
                {"Error": {"Code": "AccessDenied"}}, "operation_name"
            )
        elif exception == IOError:
            handle_csv.side_effect = ClientError(
                {"Error": {"Code": "OtherError"}}, "operation_name"
            )
        elif exception == GetDataError:
            handle_csv.side_effect = ValueError("Invalid CSV")

        with pytest.raises(exception):
            get_data(file_path)
