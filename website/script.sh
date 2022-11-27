docker build -t test_iut_website .
docker run -d -v output:/output test_iut_website