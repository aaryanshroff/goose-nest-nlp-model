terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

data "archive_file" "housing-bot" {
  type        = "zip"
  source_file = "lambda/lambda_function.py"
  output_path = "housing-bot.zip"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_housing_bot_lambda"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "lambda.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
  })
}

resource "aws_lambda_function" "scraper" {
  filename      = "housing-bot.zip"
  function_name = "HousingBot"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.iam_for_lambda.arn

  source_code_hash = data.archive_file.housing-bot.output_base64sha256

  runtime = "python3.9"
}
