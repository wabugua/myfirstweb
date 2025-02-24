{
    "version": 2,
    "builds": [
        {
            "src": "app.py",
            "use": "@vercel/python",
            "config": {
                "maxLambdaSize": "15mb"
            }
        }
    ],
    "routes": [
        {
            "src": "/static/(.*)",
            "dest": "/static/$1"
        },
        {
            "src": "/(.*)",
            "dest": "/app.py"
        }
    ],
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "production"
    }
}