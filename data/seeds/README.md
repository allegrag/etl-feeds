# Run
AWS_PROFILE=modsy python manage.py assortment -i ~/Downloads/modsy/seeds/ --dry-run

AWS_PROFILE=modsy python manage.py phoenixrugs -i ~/Downloads/modsy/seeds/ --dry-run

# Copy files
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/seeds/ s3://mcp-store-us-west-2/dev/data/seeds/ --recursive
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/seeds/ s3://mcp-store-us-west-2/staging/data/seeds/ --recursive
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/seeds/ s3://mcp-store-us-west-2/prod/data/seeds/ --recursive

# Verify copy process
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/dev/data/seeds/ --recursive
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/staging/data/seeds/ --recursive
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/prod/data/seeds/ --recursive
