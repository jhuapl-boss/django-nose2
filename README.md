#Django nose2 Custom Test Runner

** NOTE: THIS TEST RUNNER HAS BEEN CUSTOMIZED TO WORK WITH THE BOSS AND IS NOT FOR GENERAL USE **

A test runner for django 1.2 or better that runs tests with nose2.

##Setup

Django and nose dependencies have been removed from setup.py because they are managed elsewhere

In your settings.py, set:

    ```
    TEST_RUNNER="djnose2.TestRunner"
    ```

Then ``manage.py test`` will run nose2's test runner.

##Test Configuration

Three nose2 configuration files have been created:
 - `unittest.cfg`: Default config that is loaded by nose. Runs unit tests (files that start with 'test_*')
 - `inttest.cfg`: Config that is used for integration tests. Uses Layers to manage test resource setup (will only build AWS resources once). Runs all integration tests (files that start with 'int_test_*')
 - `unittest_user_defined.cfg`: Use this if you want to run specific unit tests. The `test-file-pattern` key is included to set the pattern for test discovery.
 
##Use

Put any command-line nose2 arguments for the test runner after '--'. For
example, to turn on verbose output::

  manage.py test -- -v
  
  
To run unit tests:

```
python3 manage.py test
```

To run unit tests with custom `test-file-pattern`:

```
python3 manage.py test -- -c unittest_user_defined.cfg
```

To run integration tests:

```
python3 manage.py test -- -c inttest.cfg
```

To run integration tests with verbose printing:

```
python3 manage.py test -- -c inttest.cfg -v
```


