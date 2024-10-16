from test.utils_test import test_app, get_valid_token


def test_handler_tasks_GET(test_app,get_valid_token):
    token = get_valid_token("agent-007")
    headers = {
        'Authorization': f"Bearer {token}"
        }
    res = test_app.get("/tasks", headers=headers)
    response_body = res.json

    assert res.status_code == 200
    assert response_body == [{"name": "task1"},{"name":"task2"}]

def test_handler_tasks_GET_no_bearer(test_app,get_valid_token):
    token = get_valid_token("agent-007")
    res = test_app.get("/tasks", expect_errors=True)
    response_body = res.json

    assert res.status_code == 401