AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)
AWS_DEFAULT_REGION=$(aws --profile default configure get region)

docker build -t goose-nest-nlp-model .
docker run -p 9000:8080 \
   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
   -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
   goose-nest-nlp-model
