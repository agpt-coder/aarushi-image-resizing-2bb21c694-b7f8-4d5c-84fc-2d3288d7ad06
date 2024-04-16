---
date: 2024-04-16T09:44:46.212683
author: AutoGPT <info@agpt.co>
---

# aarushi-image-resizing-2

The task involves developing a feature that processes an uploaded image according to user-defined dimensions, incorporating both resizing and optional aspect ratio maintenance through cropping. To achieve this, we'll leverage Python as the chosen programming language due to its robust support for image manipulation, alongside libraries and techniques previously identified.

**Key Requirements & Implementation Steps:**
1. Accept JPEG images from users, supporting a common use case of web-oriented image handling.
2. Utilize Python's Pillow library, which provides comprehensive tools for image resizing and cropping while maintaining excellent performance and quality outcomes.
3. Implement functionality to resize images to a target dimension of 1080x720 pixels, a size that optimally balances quality and file size for both web and print media.
4. Incorporate a cropping feature that maintains the original image's aspect ratio, should the user opt for this. This entails calculating the target aspect ratio based on user input, cropping the image accordingly, and ensuring the final image matches the desired dimensions closely without distorting the original content's proportions.
5. Apply best practices for image resizing and cropping, such as selecting the appropriate algorithm for resizing (e.g., bicubic, bilinear) to maintain quality, applying sharpening post-resize to enhance clarity, and considering the final format and compression to optimize for both quality and file size efficiency.

The development stack includes FastAPI to handle HTTP requests for image uploads and processing responses efficiently, PostgreSQL for any needed image metadata storage, and Prisma as the ORM for robust database interactions. This tech stack is selected for its ease of use, performance, and scalability, which aligns well with the project's needs for handling image manipulation tasks.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-image-resizing-2'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
