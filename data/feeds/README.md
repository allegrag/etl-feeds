# Copy files
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/feeds/ s3://mcp-store-us-west-2/dev/data/feeds/ --recursive
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/feeds/ s3://mcp-store-us-west-2/staging/data/feeds/ --recursive
AWS_PROFILE=modsy aws s3 cp ~/Downloads/modsy/feeds/ s3://mcp-store-us-west-2/prod/data/feeds/ --recursive

# Verify copy process
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/dev/data/feeds/ --recursive
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/staging/data/feeds/ --recursive
AWS_PROFILE=modsy aws s3 ls s3://mcp-store-us-west-2/prod/data/feeds/ --recursive
