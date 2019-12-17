Notes about deployment to Azure App Services

App created on Azure App Services as:

```
az webapp up --sku F1 --location "West US 2" --name motivationalboost
```

App is configured as:

```
az webapp config set --resource-group pnovak2_rg_Linux_westus2 --name motivationalboost --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 \"motivationalboost.flask_app:create_app()\""
```

The bit right at the end (`"motivationalboost.flask_app:create_app()"`) specifies how the gunicorn WSGI server should start and run the Flask app in the motivationalboost package.