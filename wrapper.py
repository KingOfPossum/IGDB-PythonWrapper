from requests import post

API_URL = "https://api.igdb.com/v4/"

class IGDB_Wrapper:
    def __init__(self, client_id: str, auth_token: str):
        """
        Initializes the IDGB_Wrapper with the client ID and authentication token needed for api requests.
        :param client_id: Client ID for IGDB API.
        :param auth_token: Authentication token for IGDB API.
        """
        self.client_id = client_id
        self.auth_token = auth_token

    def request(self,endpoint: str, query: str) -> str:
        """
        Makes a request to the IGDB API.
        :param endpoint: The endpoint
        :param query: The query to be sent to the endpoint.
        :return: The result of the request in JSON format.
        """
        url = self._construct_url(endpoint)
        params = self._get_params(query)

        response = post(url, **params)
        response.raise_for_status()

        return response.json()

    def _construct_url(self,endpoint: str) -> str:
        """
        Constructs a full URL for the given endpoint.
        :param endpoint: The endpoint to construct the URL for.
        :return: The constructed URL.
        """
        return API_URL + endpoint

    def _get_params(self,query: str) -> dict:
        """
        Constructs the parameters for the API request.
        Will include the header with the client ID and auth token, and the query data
        :param query: The query to be sent to the endpoint.
        :return: The parameters for the API request.
        """
        params = {
            'headers': {
                'Client-ID': self.client_id,
                'Authorization': 'Bearer ' + self.auth_token,
            },
            'data': query
        }
        return params