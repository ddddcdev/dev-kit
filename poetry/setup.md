# Poetry Setup (WSL Ubuntu)

## Install Required Packages
```
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git
```

## Install pyenv
```
curl https://pyenv.run | bash
```
Add the following to your ~/.bashrc or ~/.zshrc and reload the shell:
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
source ~/.zshrc  # or source ~/.bashrc
```

## Install poetry
```
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

## Add poetry plugins
```
poetry self add poetry-plugin-shell
poetry self add poetry-dotenv-plugin
poetry self add poetry-plugin-export
```

## Install Python and set it locally
```
pyenv install 3.13 # or any version you need
pyenv local 3.13
```

## Create a virtual environment in the project directory
```
poetry config virtualenvs.in-project true --local
```

## If pyproject.toml already exists
```
poetry install
```

## If you need to create pyproject.toml
```
poetry init --no-interaction
poetry install --no-root
```

## Example: Add a module with Poetry
```
poetry add pandas
```

## Example: Remove a module with Poetry
```
poetry remove pandas
```

## Typical pyproject.toml settings

Add the following to your `pyproject.toml` as needed:

```toml
[tool.dotenv]
location = ".env"
ignore = "false"

[tool.poetry]
package-mode = false

[tool.isort]
profile = "black"
line_length = 120

[tool.black]
line-length = 120
target-version = ["py3.13"]
```

## Poetry commands after updating pyproject.toml

If you manually edit or update `pyproject.toml`, run the following commands to update dependencies and the lock file:

```
poetry lock
poetry install
```

## Example: Export requirements.txt
```
poetry export -f requirements.txt --output requirements.txt --all-groups --without-hashes
```