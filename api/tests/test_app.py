import pytest

from api.app.app import create_app

def test_index_route():
    """
    GIVEN our flask app with the defined endpoints
    WHEN requesting the index page '/'
    THEN returns 404 status
    """
    app = create_app()
    response = app.test_client().get('/')

    assert response.status_code == 404