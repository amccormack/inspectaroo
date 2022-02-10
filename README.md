# About
Inspectaroo is a web app which allows users to upload images to view metadata. It is designed to show off many AWS services including EC2, Lambda, SQS, and S3. 

When users browse to the website, they have the ability to upload an image. The image will be place in S3. Upon the file hitting S3, a notification will be placed in SQS. An inspecting server listening for messages on the SQS queue will then download the image and upload the metadata back to S3. The website will see the new metadata and present it to the user.

# Source Outline

- `/website/` holds lambda code and resources for uploading image and presenting metadata from S3.
- `/inspector/` holds the code which listens for sqs messages and then processes the messages, placing the data back in s3.