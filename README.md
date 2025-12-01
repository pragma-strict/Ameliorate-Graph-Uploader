# Ameliorate Graph Uploader
Tool for uploading Ameliorate-formatted JSON graphs to [Ameliorate](https://ameliorate.app/) via its API. See [reference](https://github.com/amelioro/ameliorate/tree/main/src/api#api).

### Initial setup
1. Install python requirements (python venv optional). In repository root: `pip install -r requirements.txt`

### Usage
1.  Paste graph JSON into `graph.json` (the graph you want to upload)
2. Run `python3 upload.py` and follow the prompts (paste in session cookie when asked)
