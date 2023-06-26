# Language Translator

Frontend for [deepl api](https://www.deepl.com/en/docs-api/) made with FastAPI.

# Installation

```
https://github.com/FilipK0walewski/simple-translator
cd simple-translator
pip install -r requirements.txt
export DEEPL_API_KEY=your_api_key
uvicorn main:app --reload
```

## using docker

```
https://github.com/FilipK0walewski/simple-translator
cd simple-translator
change DEEPL_API_KEY envorontment variable in docker-compose.yaml
docker compose up
```

aplication should run on localhost:8000