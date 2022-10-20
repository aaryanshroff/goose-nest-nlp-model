cd .venv/lib/python3.10/site-packages

echo "Zipping site-packages"
zip -r -q ../../../../deployment-package.zip .
cd ../../../../

cd src

echo "Zipping src"
zip -r -g -q ../deployment-package.zip .
cd ../

echo "Deployment package created"
echo "Deploying to AWS Lambda"

aws lambda update-function-code --function-name HousingBot --zip-file fileb://deployment-package.zip