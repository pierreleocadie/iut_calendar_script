docker build -t test_iut_script_ics .
docker run -d -v output:/output test_iut_script_ics