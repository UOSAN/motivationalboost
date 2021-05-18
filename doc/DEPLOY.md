Notes about deployment to Azure App Services

App created on Azure App Services as:

```
az webapp up --sku F1 --location "West US 2" --name motivationalboost
```
To deploy updates, issue the same command as used to create the app.

Reference:
[Quickstart: Create a Python app in Azure App Service on Linux](
https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python)

App is configured as:

```
az webapp config set --resource-group sanlab_rg_Linux_westus2 --name motivationalboost --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 \"motivationalboost.flask_app:create_app()\""
```

The bit right at the end (`"motivationalboost.flask_app:create_app()"`) specifies how the gunicorn WSGI server should start and run the Flask app in the motivationalboost package.

Reference: [Configure a Linux Python app for Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/containers/how-to-configure-python#flask-app)


#### Enable logging
```
az webapp log config --resource-group sanlab_rg_Linux_westus2 --name motivationalboost --docker-container-logging filesystem
```
