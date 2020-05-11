# Image Annotator

### Tech Stack

- Django
- sqlite3 for dev DB
- html + css (md bootstrap) + jquery/js

### Run the code by the following commands

```python
    python manage.py migrate
    python manage.py runserver
```

### Go to http://127.0.0.1:8000/ or http://localhost:8000/

### Usage

- Login into the app at http://127.0.0.1:8000/auth/login/

  ![upload image](./output/17.png)

* If it is the first time register here http://127.0.0.1:8000/auth/register/

  ![upload image](./output/16.png)

* After login, Go to http://127.0.0.1:8000/upload-images/ to upload images, enter the project name to which the images are to be saved.

* Drag and drop or upload multiple images and hit submit

  ![upload image](./output/11.png)

  ![upload image](./output/10.png)

* Go to http://127.0.0.1:8000/all-images/ to view uploaded images

* click on the image you want to annotate

  ![upload image](./output/13.png)

* It will go to a new page, where you can annotate the image

  ![upload image](./output/14.png)

* Annotate the image and hit submit to save the image to DB, it will save the data to DB and redirect to the previous page, where you can view the annotated images below

  ![upload image](./output/7.png)

* click on the annotate image to view the annotations and download the **.csv file**

  ![upload image](./output/8.png)

* click the download button to download the csv file

  ![upload image](./output/9.png)

* To view all the Projects
  go to http://127.0.0.1:8000/view-all-projects/

  ![upload image](./output/15.png)

  - To view all the images specific to a particular project click on the link to **View all project related images**
