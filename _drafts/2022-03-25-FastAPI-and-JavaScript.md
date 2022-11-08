---
date: "2022-03-25"
title: "FastAPI and JavaScript"
---
<!-- filename "2022-03-25-FastAPI-and-JavaScript.md" -->

<!-- markdownlint-disable MD025 -->
# FastAPI JavaScript
<!-- markdownlint-enable MD025 -->

## Simplest Front End / Back End

`main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:9000"]

# assumes a suitable web server, e.g. "python -m http.server 9000"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Run `uvicorn main:app --reload` in the diretory with `main.py`

`index.html`

```html
<!DOCTYPE html>
<html>

<head>
    <script>
        function getMessage() {
            fetch('http://localhost:8000')
                .then(function (response) { return response.json() })
                .then(function (data) {
                    document.getElementById("replaceable_text").innerHTML = data.message
                });
        }
    </script>
</head>

<body>

    <p>Run a suitable web server that is allowed by CORS, for instance:
        <code>python -m http.server 9000</code>

    <p id="replaceable_text">Text to be replaced by FastAPI</p>

    <button type="button" onclick="getMessage()">Replace text</button>

</body>

</html>
```

run `python -m http.server 9000` in the directory with `index.html`

## Front End

[CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/) for a front end with a different signature from the back end
[Official Docker Image with Gunicorn - Uvicorn](https://fastapi.tiangolo.com/deployment/docker/#official-docker-image-with-gunicorn-uvicorn)

## Download stuff to a file from javascript

[Blob](https://javascript.info/blob)

```javascript
function download(thing, filename = 'download'){
    let link = document.createElement('a');
    link.download = filename;

    let blob = new Blob([thing]);

    link.href = URL.createObjectURL(blob);

    link.click();

    URL.revokeObjectURL(link.href);
}   
```

## Working with NodeLists

```javascript
// https://jshint.com/docs/options
let t = document.querySelector("table"); // first table, should be the enforcing one
let ids = Array.from(t.querySelectorAll("tr>td[id]")); // the ids
let filtered = ids.filter(i => !i.parentElement.innerHTML.includes('deprecated'));
let strictOptions = filtered.map(i => {return i.id + ": true"}).join(", ");
```

## Classes

[Simple “Class” Instantiation](https://johnresig.com/blog/simple-class-instantiation/)
[JavaScript without “new” and “this”keywords](https://nemisj.com/js-without-new-and-this/)

## Links

* [{JSON} Placeholder](https://jsonplaceholder.typicode.com)
* [FastAPI](https://fastapi.tiangolo.com/)
* [petite-vue](https://github.com/vuejs/petite-vue)
* [Project Generation - Template](https://fastapi.tiangolo.com/project-generation/)
* [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/)
* [Build FastAPI + uvicorn + nginx with docker-compose](https://linuxtut.com/en/02ed76b94c60deba8282/)
* [The cheap way how to use Docker to deploy your FastAPI](https://medium.com/analytics-vidhya/how-to-deploy-a-python-api-with-fastapi-with-nginx-and-docker-1328cbf41bc)
* [GitHub Copilot](https://copilot.github.com)
* [Learn JavaScript](https://github.com/snipcart/learn-vanilla-js)
* [JavaScript Helper Functions](https://vanillajstoolkit.com/helpers/)
* [JavaScript Libraries](https://vanillajstoolkit.com/libraries/)

<!-- markdownlint-disable MD034 -->
https://vuejs.org/
https://fastapi.tiangolo.com/deployment/docker/
<!-- markdownlint-enable MD034 -->