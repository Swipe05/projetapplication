import requests

key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNkZWU5YmZjLTAwNDItNDcwMy1hMzI2LWMwNmZkZjUzODEyZSIsImlhdCI6MTY1NTcxMjU3MCwic3ViIjoiZGV2ZWxvcGVyLzgxMzZlZTYzLTQ2MzctNjQ1Yy1iMTdjLWMwMDliZWUxMWY0ZSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTUuMjIxLjM4LjI1NCJdLCJ0eXBlIjoiY2xpZW50In1dfQ._EMIyRqIwJmYclGrSJLBZwMMA24n9fR7UE0AJs780776Ji16x6R901buTg-enNImLz7Et4RH6f118QJYj2Srlg'
headers = {
    'Accept': 'application/json',
    'authorization' : 'Bearer ' + key
}


def get_user(tag):
    #return user profile information
    response = requests.get(f'https://api.clashroyale.com/v1/players/%23{tag}', headers=headers)
    user_json = response.json()
    print(user_json['name'])

def search_clan():
    pass
    #submit a clan search

get_user('J90UG8V')

