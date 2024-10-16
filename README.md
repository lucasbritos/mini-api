```
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt

sed -i '' '/^# Prompt customization/a\
export PYTHONPATH=$(pwd)/src 

python src/containers/local/server.py
python -m debugpy --listen localhost:5678 --wait-for-client src/containers/local/server.py
python -m debugpy --listen localhost:5678 --wait-for-client -m pytest



terraform init
terraform workspace new develop
terraform apply -var-file=develop.tfvars
terraform apply -var-file=$(terraform -chdir=tf workspace show).tfvars

terraform apply
```
