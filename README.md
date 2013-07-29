# Spending Stories
## Architecture 
<pre style="line-height:1em; font-size:0.8em">
  <code>
[Backend]                          +----------------+
                          +------->| Admin          |
                          |        |----------------|
                      +-------+    | Admin Forms    |-django-contrib-admin
                      | CRUD  |    |                |
                      +-------+    |                |
                          |        +----------------+
                          v
 +--------+         +----------+                   +-----------------+
 |Database|         | Core     |    +--------+     | API             |
 |--------|x--SQL--x|----------|    | Create |     |-----------------|-django-filters
 |        |         | Models   |x---| Read   |----x| REST ressources |-django-rest-framework
 |        |         | Forms    |    | Update |     | Serializers     | |
 |        |         |          |    +--------+     |                 | +--docs
 +--------+         +----------+                   |                 |
                                                   |                 |
 +-------------------+                             |                 |
 | Static            |                             +-----------------+
 |-------------------|                                           ^
 |Templates          |--coffeescript---+                         |
 |Scripts (coffee+js |                 |                         |
 |Styles (less+css)  |                 |                         |
 |Files (img+csv)    |-----+           |                     HTTP/JSON
 |                   |     |           |                         |
 +-------------------+     |           |                         |
     |             Django Templates    |                         |
+----|---------------------|-----------|-------------------------|-----------------------------+
    Less                   |           |                         |                     Frontend]
     |                     |           v                         v
     v                     |      +--------------------------------------------+
    +-----+-boostrap       |      |JavaScript   |                              |-jQuery
    | css |-other mixins   |      |-------------+                              |
    +-----+                v      |                                            |-AngularJS
                       +-------+  |        +-----------+       +-------------+ |
                       | html  |x---feed--x| ng-Models |x-use-x|  APIClient  | |
                       +-------+  |        +-----------+       +-------------+ |
                                  |                                            |
                                  +--------------------------------------------+
</code>
</pre>
## About 

### Recommended Tools

- Sublime Text 2, the light-speed-hard-rocking text editor
- [autoenv](https://github.com/kennethreitz/autoenv) to activate your virtual 
  environnement when enterring the project folder 

### Code Conventions

If you want ton contribute to this projet please follow the [jplusplus styeguide](https://github.com/jplusplus/styleguide).

## How to install
### 1. Set up your python environnement

**a. Install python packages:**

```bash
sudo apt-get install build-essential python python-pip python-dev mysql nodejs npm libapache2-mod-wsgi
```

**b. Install virtualenv**

```bash
sudo pip install virtualenv
```

**c.** *(optional)* **use [autoenv](https://github.com/kennethreitz/autoenv) & [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to ease your life**

**d.  Create the virtualenv folder folder for this project:**
  > Every dependencies will be installed in this folder to keep your system's environnement clean.

At project's root run this command. 

```bash
virtualenv venv --distribute --prompt=SpendingStories
```

**e. Activate virtualenv:**
If you installed autoenv you just need to reenter the project root: 

```bash
cd .
```
Else you have to run: 

```bash
source venv/bin/activate 
```


### 2. Install dependencies
**a. Install python modules required**

```bash
pip install -r requirements.txt
``` 

**b. Install preprocessors for *Less* and *CoffeeScript***
    
```bash
cat npm_requirements.txt | sudo xargs npm -g install
```






