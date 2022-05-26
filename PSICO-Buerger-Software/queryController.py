import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cert = {
  "type": "service_account",
  "project_id": "psico-software",
  "private_key_id": "29aeb88d7fe188b6e8e7e4aa40bfa2e1346a8076",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDSpcbxqpkbLBNW\noP4XZdISAQql0cHdI9g+23MOMJxOWkick31pOL/21+xggMr8mQis9nR9LkUJnAQ7\nOQRpfMpQfDa4Q4cq7LE6cGknrjHfs8tMdQ7h/+PjYwvR8+saC4DKGq0/TiTQh/5F\npGh5zZF6pyPIYNhTBc36G2ilYGvMY2RJAWX7EiQugC0IbO7heafI692BLnDpCj+U\nih7/bCOagzIB8WhuVYBnkkP7YlwyT/qnKcTU56Rles+MGzJRGDNbduphXzwTLjd8\nQjtSyBejtJ5tf9+79L9bAdKe/wKBzw5AErF6YzKOfm/wRBmYyKtMsze2HYSTs5XY\n6xXVkvfnAgMBAAECggEAIlCHHA8iad7AN7h6K+2WTwCEb4bAAfo42+R71a/thoYG\nlhsgrudjvh5mj0Hrz0JOu35ac5n5/RrBRbSAF38QphPWBiZZ+pAcPtzZBHHIBh0P\n3SCkkARTZ1NXNZh6j/+Xt1SpLErajG3a6hViP5VRQZ3Aon/EPaIQb9HPNkGCzgSH\nQ/rBbO1eMZy8BoAfybZzNX2qs+Skdw0XS5Nuf+1yywJpfnRH/vvFzmvzy9EdZ/AP\ncMJEU7WdjF8hY/SDpVASiqEnBlq8FZM5W/xnbKlMjm3CYk6C4m156FJfs7GQjlfr\n/VZfdsMxVBrbQnD8znBosYJeNDSjKX+bLKwS4qEFoQKBgQDqxqQIapRoRQM26MUP\nn2EoforIfGcEXvMxJerd8hjfHldBaX9b1NHkdCqPuRIOArQgVM2Hbxb77+pUAIhR\nyaj/azPcH3d/VaZJp4mpJurvoUxMRKc6poFyMyajtSGwRrtuXXPdszVDSRY6q3Xw\nzKx67cVuWPoU+fQIL6IogyYTdQKBgQDlsL1YAkbLkiJgm90M91LKxyUhQi5VVcdL\nOhcyAjNDIZkUixITCy4hB5npNdKgQ8/ar4y/UQz1hzJYv+XzMFlu9UHE5LqAl/LO\nGgapKmhlsKGoxSsCGZDucYNS1R3FVQ728mPR1R6V/XcvrK0uqXSMZ3zmdemdHAgl\nTEOpili+awKBgFeS7RDuoJkcVQygWxFuxBEU0rPiI5Mvz8sfd7J+YeSoLqgJsCYT\nBpAO/OlLgX6UZ5g/ycKhH5OudFwNLsxDSrSrylZrrmljC3oh8mmUSMJGCm3Qlgh8\nn4B3sAwUvpJAcB3E4jlqZY3Jr28HEiFWV2grVR/KNM6qRerfyb8O3J8ZAoGAODkc\n/+/+uFHbDF7aqxPXNj+s/QkgIk9O60Ea8GjNd38/42FvWS4BaqBbslQ0bHps5JDY\nGPSUAX3IeyTt+qs5GQn7wWBjrpqDGqQQQVRaHZow2Aj7UBZF/bfXd20nTmhVs2j9\nuh060WgrxoW0FpnwJ3YlgpwWRRjZfZe/cD6nHmUCgYArZDoYkTw7gWGZxWEEcO9a\nPMaL2jMO/4a9ldjwfF85uJrWZ2XE3UJs7GaKn7GtLU9RNqOLMChU35XaMKVZQ9i9\nn+l0p8huzh+bB1FGP/ypL3rAPFtmuCZclMIzQ7lnp/lBNmKVe/SZnu9tvVB2MKDU\nzhJWWF1dasYUzKEptxlHuQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-9nkfp@psico-software.iam.gserviceaccount.com",
  "client_id": "112691732338397025836",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9nkfp%40psico-software.iam.gserviceaccount.com"
}

cred = credentials.Certificate(cert)
firebase_admin.initialize_app(cred, {
    'projectId': 'psico-software',
})

db = firestore.client()

USER_STORAGE_REF = db.collection(u'Citizen-Storage')
REF = USER_STORAGE_REF.stream()

for doc in REF:
    print(f'{doc.id} => {doc.to_dict()}')

class QueryController():
    def __init__(self) -> None:
        self.instance = 1

    def updateQuery(citizen):
        pass

    def insertQuery() -> int:
        pass

    def selectQuery(id):
        pass