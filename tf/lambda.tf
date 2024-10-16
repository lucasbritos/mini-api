# Calculate the source code hash separately
locals {
  lambda_hash = filebase64sha256("../dist/lambda.zip")
  layer_hash = filebase64sha256("../dist/lambda-layer.zip")

}


# Create IAM Role
resource "aws_iam_role" "lambda_role" {
name   = "myapp-api-py-lambda-function-role-${terraform.workspace}"
assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "lambda.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

# Create IAM Policy
resource "aws_iam_policy" "iam_policy_for_lambda" {
 name         = "aws-iam-policy-for-myapp-api-py-lambda-function-role-${terraform.workspace}"
 path         = "/"
 description  = "AWS IAM Policy for managing aws lambda role"
 policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
                "dynamodb:Query",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutObject"
          ],
          "Resource": [
              "arn:aws:logs:*:*:*",
              "${aws_dynamodb_table.tasks.arn}",
              "${aws_dynamodb_table.tasks.arn}/index/*",
              "${aws_s3_bucket.results.arn}",
              "${aws_s3_bucket.results.arn}/*"
          ]
        }
    ]
}
EOF
}

# Attach IAM Policy to IAM Role
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
 role        = aws_iam_role.lambda_role.name
 policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "aws_lambda_function" "lambda_func" {
  filename                       = "../dist/lambda.zip"
  function_name                  = "myapp-api-py-${terraform.workspace}"
  role                           = aws_iam_role.lambda_role.arn
  handler                        = "containers.lambda.handler.lambda_handler"
  runtime                        = "python3.8"
  source_code_hash               = local.lambda_hash
  layers = [aws_lambda_layer_version.lambda_layer.arn]
  architectures                  = ["arm64"]
  timeout                        = 30 
  depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  environment {
    variables = {
      AUTH_REQUEST = var.AUTH_REQUEST
      SERVER_DEBUG = var.SERVER_DEBUG
      REMOTE_JWKS_ENDPOINT = var.REMOTE_JWKS_ENDPOINT
      LOGGING_LEVEL = var.LOGGING_LEVEL
      ENVIRONMENT = terraform.workspace
    }
  }
}

resource "aws_lambda_function_url" "function_url" {
  function_name      = aws_lambda_function.lambda_func.function_name
  authorization_type = "NONE"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "../dist/lambda-layer.zip"
  layer_name = "myapp-api-py-layer"

  source_code_hash    = local.layer_hash
  compatible_runtimes = ["python3.8"]
  compatible_architectures = ["arm64", ]
  skip_destroy = true
}

output "function_url" {
  description = "function URL"
  value = aws_lambda_function_url.function_url.function_url
}