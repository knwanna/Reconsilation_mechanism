def test_reconciliation_scoring(client):
    response = client.post("/reconcile", json={"query": "python"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["score"] >= 0.5  # Minimum confidence threshold

def test_content_type_filtering():
    from core.domain import reconciliation
    results = reconciliation.reconcile("python", content_type="youtube")
    assert all(r.content_type == "youtube" for r in results)