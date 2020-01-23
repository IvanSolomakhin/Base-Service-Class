# Base-Service-Class
Module for creating services, transferring requests and responses between them using the base class Service.
Developed and maintained on **Python 3**

**Service class** 

Base service class.
```python
class Service(object)
```
Service constructor.<br/>
  [in] name - Service name.<br/>
	[in] workerTimeout - Service worker timeout.<br/>
	[in] numWorkerThreads - Count of service worker threads.<br/>
	[in] jobQueueMaxSize - Service job queue max size.
  
```python
def __init__(self, name, workerTimeout = 1, numWorkerThreads = 16, jobQueueMaxSize = 100)
```
Service destructor. Joins worker threads.
```python
def __del__(self)
```
Starts service. Runs worker threads.
```python
def start(self)
```
Stops Service. Joins worker threads.
```python
def stop(self)
```
Gets service state.<br/>
[out] true - Service is running.<br/>
[out] false - Service is stopped.<br/>
```python
def state(self)
```
Sends request to service.<br/>
[in] package - Contained method and arguments to call in request service.<br/>
```python
def sendRequest(self, package)
```
Sends responce to service.<br/>
[in] package - Contained method and arguments to call in response service.<br/>
```python
def sendResponse(self, package)
```

**Package class** 

Container for transfering data between services.
```python
class Package(object)
```
Package constructor.<br/>
[in] requestServiceName - Request service name.<br/>
[in] requestMethod - Request method in service.<br/>
[in] requestArguments  - Request arguments for method, can be ignored.<br/>
[in] responseServiceName - Response service name, can be ignored.<br/>
[in] responseMethod - Response method in service, can be ignored.<br/>
```python
def __init__(self, requestServiceName, requestMethod,requestArguments = None,
  responseServiceName = None, responseMethod = None)
```

**Example run** 

Example of using base Service class.

```
user@user-lws$ python3 example.py 
[DEBUG, 22-Jan-20 14:22:51] __init__: Calculator
[DEBUG, 22-Jan-20 14:22:51] __init__: User
[DEBUG, 22-Jan-20 14:22:51] start: Calculator
[DEBUG, 22-Jan-20 14:22:51] start: User
[DEBUG, 22-Jan-20 14:22:52] askPlusOperation: 34, 21
[DEBUG, 22-Jan-20 14:22:52] sendRequest: User to Calculator, plusOperation
[DEBUG, 22-Jan-20 14:22:52] __worker: Calculator call plusOperation
[DEBUG, 22-Jan-20 14:22:52] plusOperation: 34, 21
[DEBUG, 22-Jan-20 14:22:52] sendResponse: Calculator to User, onPlusOperationDone
[DEBUG, 22-Jan-20 14:22:52] __worker: User call onPlusOperationDone
[DEBUG, 22-Jan-20 14:22:52] onPlusOperationDone: 34 + 21 = 55
[DEBUG, 22-Jan-20 14:22:53] stop: Calculator
[DEBUG, 22-Jan-20 14:22:54] stop: User
[DEBUG, 22-Jan-20 14:22:55] __del__: Calculator
[DEBUG, 22-Jan-20 14:22:55] __del__: User
```

**Unittests** 

Provided unit tests for service module.

```
user@user-lws$ python3 -m unittest -v test
testSendJobs (test.TestService) ... ok
testSendNone (test.TestService) ... ok
testSendNoneWithoutResponse (test.TestService) ... ok
testSendNumber (test.TestService) ... ok
testSendPair (test.TestService) ... ok
testSendTuple (test.TestService) ... ok
testStartStop (test.TestService) ... ok

----------------------------------------------------------------------
Ran 7 tests in 13.323s

OK
```

