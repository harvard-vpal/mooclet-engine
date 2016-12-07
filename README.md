# mooclet-engine
A web service for creating and using MOOClets.

## Background

### What is a MOOClet?
A MOOClet is a digital component – like an explanation in an online course or problem – designed using the MOOClet technology. This technology enables instructors and researchers to engage in a wide range of A/B experimentation, crowdsourcing, real-time data analysis, and personalization. 

The term MOOClet is used because this technology was first developed for MOOCs – the framework can be used to redesign any digital resource – this webpage, emails, components of smartphone apps.

See http://www.josephjaywilliams.com/mooclet for a comprehensive definition.

### MOOClet engine
This application, built with Python Django, provides a web service that a user or application can interact with via a RESTful API, enabing the creation and use of MOOClets.

## Setup
### Local setup

Install required packages for local development:
```
  # Install from requirements file
  pip install requirements_local.txt
```
Fill in the required Django settings in  ```mooclet_engine_app/settings/secure.py``` based on the template files.

Start up the application:
```
  # Start the web server
  python manage.py runserver
```

### Deployment on AWS Elastic Beanstalk
Create an AWS account and install the [Elastic Beanstalk Command Line Interface (EB CLI)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) if needed.

Fill in the necessary settings in ```mooclet_engine_app/settings/secure.py``` and ```.ebextensions/secure.config``` based on the provided template files.

Deploy the application:
```
# Initialize the Elastic Beanstalk project
eb init
# Create a new envrionment and deploy
eb create
```
See AWS's guide to [Deploying a Django Application to Elastic Beanstalk](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html) for more details.

## Usage
See [this spreadsheet](https://docs.google.com/spreadsheets/d/1cmnQff9T7o2KhaccvdoLNj4v9lGaWpoxkPJ2nEUM_Ow) for a list of supported API endpoints and examples.
