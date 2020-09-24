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

<details>
  <summary>test & coverage</summary>
  
  to run basic pytest:
  ```
  pytest
  ```
  ---
  to use coverage run:
  ```
  coverage run -m pytest
  ```
  when the test above is done:
  ```
  coverage html
  ```
  this will create a new folder 'htmlcov' in the project dic, in 'htmlcov' open index.html to see full data of the coverage.
</details>

### completed:
* Site skeleton, and basic functionality. 
  
* <details>
    <summary>Tests and full coverage.</summary>

    Pytest to all the function and pages so far and getting 100% coverage(all the script is being tested).
    Every new function will be added to the tests when setting up the function.
    
   </details>

* <details>
    <summary>Database maneging and only logged user allowed to change the database.</summary>
    
    Only when a user is lodged in, his data will be pulled from the database and only he can see and change his data. 
    
    Full user interaction:
    * register.
    * log in and out.
    * profile page with image upload, password change and account delete option.
    
    </details>
    
  
* <details>
    <summary>ToDo list work both with logged and not logged user.</summary>
    
    Todo List page automatically use the logged or not logged variation, with the logged in variation pull the user task from the database and shown to the user. All task can be set to "complete" and deleted at any time.  
    The logged in ToDo list use jQuery post to keep the page updated and not load again on every change made.

    </details>
    
* <details>
    <summary>CSS to all the pages so far.</summary>

    Basic CSS to the site to take it out of it's default html look. Must likely its final look as the CSS is not my main focus for now.  
    
   </details>

* <details>
    <summary>Server and site setting.ini implementation. </summary>
    
    Reading the setting from the ini file and set up the server launch accordingly. Includes debug mod, public or privet open site, email and email password and user "Remember me" time when login in.  
    When there is no setting.ini at server launch create new file and use default setting. 
    
    </details>
    
* <details> 
    <summary>Email code to reset password (forgot password).</summary>

    When there is email and password in the setting.ini auto enable the reset password function. "Forgot password" link automatically added to the login page. Using the given mail and password send the registered E-mail its rest code and link to continue the reset process.  
    The user link and code is random, personal and time limited.  
    
   </details>
   
### working on:
* GUI for the site start with build in option changes.

##### More ideas:
* add weather widget (local and multi locations), both logged and not logged same as the ToDo list.
* pass-time mini games. (probably best to be JavaScript so unlikely to happen, mainly want to focus on python).
