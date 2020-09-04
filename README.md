# FlaskWebsiteProject
work in progress
### setup and run:
<details>
  <summary>Setup</summary>
  This guide is based on windows console.  
  
  set up the environment:  
  ```
  py -m venv venv
  ```
  starting the environment:  
  ```
  venv\Scripts\activate
  ```
  install the needed libraries:
  ```
  pip install .
  ```
  to fully use and see the project tests and coverage:
  ```
  pip install .[test]
  ```  
  
</details>

<details>
  <summary>running</summary>
  
  run the flask server using:
  ```
  py web_launch.py
  ```
  
</details>

### completed:
* site skeleton, and basic functionality.
* tests and full coverage.
* database maneging and only logged user allowed to change the database.
* ToDo list work both with logged and not logged user.
* CSS to all the pages so far, may take some time.

### working on:
* GUI for the site start with build in option changes.

### Next up:
* email code to reset password (forgot password).

##### More ideas:
* add weather widget (local and multi locations), both logged and not logged same as the ToDo list.
* search bar to multi search engines.
* pass-time mini games. (probably best to be JavaScript so unlikely to happen, mainly want to focus on python).
