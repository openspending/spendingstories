# Spending Stories
## Architecture 
    [Backend]                          +----------------+
                              +------->+ Admin          |
                              |        |----------------|
                          +---+---+    | Admin Forms    |-django-contrib-admin
                          | CRUD  |    |                |
                          +---+---+    |                |
                              |        +----------------+
                              v
     +--------+         +----------+                   +-----------------+
     |Database|         | Core     |   +--------+      | API             |
     |--------|<--SQL-->|----------|   | Create |      |-----------------|
     |        |         | Models   |<--| Read   |----->| REST ressources |-django-rest-framework
     |        |         | Forms    |   | Update |      | Serializers     | |
     |        |         |          |   +--------+      |                 | +--docs
     +--------+         +----------+                   |                 |
                                                       |                 |
     +-------------------+                             |                 |
     | Static            |                             +-----------------+
     |-------------------|                                      ^
     |Templates          |--coffeescript---+                    |
     |Scripts (coffee+js |                 |                    |
     |Styles (less+css)  |                 |                    |
     |Files (img+csv)    |                 |                    |
     |                   |                 |                HTTP/JSON
     +-------------------+                 |                    |
        |             |                    |                    |
    +---|-------------|--------------------|--------------------|----------------------------------+
        |             |                    |                    |                          Frontend]
        |             |                    v                    |
        |             |               +-------------+-AngularJS |
       Less     Django Templates      |JavaScript   |-jQuery    |
        |             |               +----+---+----+           |
        |             |                    |   |                |
        |             |                    |   |                |
        |             v                    |   |                v
        |         +----------------+       |   |            +-------------+
        |         | html           |       |   +------------+  APIClient  |
        |         +----------------+       |                +-------------+
        v                    ^             |                     ^
      +-----+-boostrap       |         +---+-------+             |
      | css |-other mixins   +feed---->| ng-Models |<-----use----+
      +-----+                          +-----------+

## About 

### Recommended Tools

- Sublime Text 2, the light-speed-hard-rocking text editor
- [autoenv](https://github.com/kennethreitz/autoenv) to activate your virtual 
  environnement when enterring the project folder 

### Code Conventions

- [Tabs are evil](http://www.emacswiki.org/emacs/TabsAreEvil) use `4` spaces instead
- Always save in UTF-8;
- Use UNIX line endings;
- A code line **should be** less than `80` caracters and **never** exceed `100` caracters  
- Empty lines are used to separates blocks of functionnality (like functions), don't overuse them
- Don't comment a line of code without a comment explaning why 
- Comments are good as they are representative of the code commented, in other terms: **watch your old comments**
- Class names are in `CamelCase`
- Function and methods are in `underscore_fashion()`
- Constants are in `UNDERSCORE_UPPERCASE_FASHION`
- Function scope variables are in `underscore_fashion`
- [The best code is no code at all](http://www.codinghorror.com/blog/2007/05/the-best-code-is-no-code-at-all.html)


## Install 

### Dependencies 
- Python >= 2.7
- PostgreSQL 
- fabric 




##### Install PostgreSQL

```bash
sudo apt-get build-dep python-psycopg2
```

