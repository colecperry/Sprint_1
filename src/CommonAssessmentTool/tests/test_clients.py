from fastapi import status

# Constants for common test data
VALID_USER_ID = 1
INVALID_USER_ID = 999
VALID_CASE_WORKER_ID = 2
VALID_CLIENT_ID = 1
INVALID_CLIENT_ID = 999
MIN_SUCCESS_RATE = 70


# Test GET Operations
def test_get_clients_unauthorized(client):
    """Test that unauthorized access is prevented"""
    response = client.get("/clients/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_clients_as_admin(client, admin_headers):
    """Test getting all clients as admin"""
    response = client.get("/clients/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "clients" in data
    assert "total" in data
    assert len(data["clients"]) > 0


def test_get_client_by_id(client, admin_headers):
    """Test getting specific client"""
    response = client.get(f"/clients/{VALID_CLIENT_ID}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == VALID_CLIENT_ID

    response = client.get(f"/clients/{INVALID_CLIENT_ID}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_clients_by_criteria(client, admin_headers):
    """Test searching clients by various criteria"""
    response = client.get(
        "/clients/search/by-criteria", params={"age_min": 25}, headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0

    response = client.get(
        "/clients/search/by-criteria",
        params={"age_min": 25, "currently_employed": True, "gender": 2},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        "/clients/search/by-criteria",
        params={"age_min": 15},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_clients_by_services(client, admin_headers):
    """Test getting clients by service status"""
    response = client.get(
        "/clients/search/by-services",
        params={"employment_assistance": True, "life_stabilization": True},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_client_services(client, admin_headers):
    """Test getting services for a specific client"""
    response = client.get(f"/clients/{VALID_CLIENT_ID}/services", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    services = response.json()
    assert isinstance(services, list)
    assert len(services) > 0
    assert "employment_assistance" in services[0]
    assert "success_rate" in services[0]


def test_get_clients_by_success_rate(client, admin_headers):
    """Test getting clients by success rate threshold"""
    response = client.get(
        "/clients/search/success-rate",
        params={"min_rate": MIN_SUCCESS_RATE},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_clients_by_case_worker(client, admin_headers, case_worker_headers):
    """Test getting clients assigned to a case worker"""
    response = client.get(
        f"/clients/case-worker/{VALID_CASE_WORKER_ID}", headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        f"/clients/case-worker/{VALID_CASE_WORKER_ID}", headers=case_worker_headers
    )
    assert response.status_code == status.HTTP_200_OK


# Test UPDATE Operations
def test_update_client(client, admin_headers):
    """Test updating client information"""
    update_data = {"age": 26, "currently_employed": True, "time_unemployed": 0}
    response = client.put(
        f"/clients/{VALID_CLIENT_ID}", json=update_data, headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    updated_client = response.json()
    assert updated_client["age"] == 26
    assert updated_client["currently_employed"] is True
    assert updated_client["time_unemployed"] == 0


# Test Create Case Assignment
def test_create_case_assignment(client, admin_headers):
    """Test creating new case assignment"""
    response = client.post(
        f"/clients/{VALID_CLIENT_ID}/case-assignment",
        params={"case_worker_id": VALID_CASE_WORKER_ID},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        f"/clients/{VALID_CLIENT_ID}/case-assignment",
        params={"case_worker_id": VALID_CASE_WORKER_ID},
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Test DELETE Operation
def test_delete_client(client, admin_headers):
    """Test deleting a client"""
    response = client.delete(f"/clients/{VALID_CASE_WORKER_ID}", headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/clients/{VALID_CASE_WORKER_ID}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.delete(f"/clients/{INVALID_CLIENT_ID}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
