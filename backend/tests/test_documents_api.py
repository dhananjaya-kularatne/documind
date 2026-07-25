from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_FILE_1 = r"C:\Users\mrdha\OneDrive\Pictures\Documents\tes1.pdf"
TEST_FILE_2 = r"C:\Users\mrdha\OneDrive\Pictures\Documents\Receipt.pdf"


def test_upload_two_documents_into_one_session():
    with open(TEST_FILE_1, "rb") as f1, open(TEST_FILE_2, "rb") as f2:
        response = client.post(
            "/documents",
            files=[
                ("files", ("tes1.pdf", f1, "application/pdf")),
                ("files", ("Receipt.pdf", f2, "application/pdf")),
            ],
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    session_id = data[0]["session_id"]
    assert data[1]["session_id"] == session_id  # both share one session

    filenames = {doc["filename"] for doc in data}
    assert filenames == {"tes1.pdf", "Receipt.pdf"}


def test_ask_question_across_session_returns_citations_from_both_files():
    with open(TEST_FILE_1, "rb") as f1, open(TEST_FILE_2, "rb") as f2:
        upload_response = client.post(
            "/documents",
            files=[
                ("files", ("tes1.pdf", f1, "application/pdf")),
                ("files", ("Receipt.pdf", f2, "application/pdf")),
            ],
        )
    session_id = upload_response.json()[0]["session_id"]

    ask_response = client.post(
        f"/sessions/{session_id}/ask",
        json={"question": "What are these documents about?", "document_ids": None},
    )

    assert ask_response.status_code == 200
    data = ask_response.json()
    assert data["answer"]
    assert len(data["sources"]) > 0
    for source in data["sources"]:
        assert "filename" in source