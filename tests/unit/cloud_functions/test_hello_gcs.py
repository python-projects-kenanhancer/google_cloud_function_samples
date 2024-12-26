from cloudevents.http import CloudEvent

from cloud_functions import hello_gcs


class TestHelloGcs:
    def test_hello_gcs_prints_details(self, capsys):
        """
        Ensures that hello_gcs prints the correct details when
        triggered by a CloudEvent with relevant data.
        """
        # Define CloudEvent attributes
        attributes = {
            "id": "1234-1234-1234",
            "source": "//storage.googleapis.com/projects/_/buckets/my-bucket",
            "specversion": "1.0",
            "type": "google.cloud.storage.object.v1.finalized",
        }

        # Define CloudEvent data payload
        data = {
            "bucket": "my-bucket",
            "name": "file.txt",
            "metageneration": "1",
            "timeCreated": "2021-04-23T07:00:00.000Z",
            "updated": "2021-04-23T07:00:00.000Z",
        }

        # Create the CloudEvent
        event = CloudEvent(attributes, data)

        # Invoke the function
        hello_gcs(event)

        # Capture stdout (print statements)
        captured = capsys.readouterr()
        output = captured.out

        # Assertions to verify the output text
        assert "Event ID: 1234-1234-1234" in output
        assert "Event type: google.cloud.storage.object.v1.finalized" in output
        assert "Bucket: my-bucket" in output
        assert "File: file.txt" in output
        assert "Metageneration: 1" in output
        assert "Created: 2021-04-23T07:00:00.000Z" in output
        assert "Updated: 2021-04-23T07:00:00.000Z" in output
