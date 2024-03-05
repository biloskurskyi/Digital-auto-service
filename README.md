# Digital-auto-service

DAS is a project aimed at automating car services. With just a two-minute registration process, you can easily and freely manage your own auto service.  
In addition, as the owner, you have full permissions for six categories: managers, clients, cars, workers, orders, and stations. You can create/read/update/delete any of them.   
Furthermore, you have the option to download all information about your company in a PDF file. ALso, you'll find statistic about your company available from the side.   
Moreover, managers can log in and work with your company. Once created, each manager receives all the necessary data via email. They can't see other managers' information, have limited options, and can't change info about stations.  

The project was developed using Django 4 (Python 3) and incorporates PostgreSQL, Redis, Celery, HTML, CSS, and AJAX. The code adheres to PEP8 standards for Python, ensuring clean and readable code.  
The project follows the MTV (Model-Template-View) architecture, with all database class tables defined in the models file and stored in PostgreSQL. An ORM simplifies writing queries in code files.  
Database data is incorporated into templates using Jinja. Templates are located in the 'templates/app_name' directory, while CSS, fonts, images, JavaScript, and plugins are stored in the 'static/vendor' folder.  
Each app resides in its own folder, containing directories for migrations and templates, along with Python files for models, views, forms, tasks, tests, apps, admin, init and urls. The main folder for settings is named 'DAS'.
     
On this project worked:   
https://github.com/biloskurskyi    
https://www.linkedin.com/in/valerii-biloskurskyi-175429281/   

