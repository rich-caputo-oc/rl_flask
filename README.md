# rl_flask

### Set up
- Download repo to local machine
- Navigate to repo directory
- `cp src/utils_ext_base.py src/utils_ext.py`
- Edit `src/utils_ext.py` as necessary to define your specific problem
  - Look for `# YOUR CODE HERE` comments
- `docker-compose build`
- `docker-compose up` with optional `-d` parameter to run detached
- If not in a local dev environment, change `FLASK_DEBUG: 0` in `docker-compose.yml`
- Run `localhost:4000/get_action?state=<current_state>` to get optimal action
- Run `localhost:4000/update?action=<current_action>&reward=<current_reward>` with optional `&state=<current_state>` to train model and get next state.