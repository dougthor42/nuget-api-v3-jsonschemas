# NuGet API v3 JsonSchemas
This repo contains the JsonSchema files that can be used to validate
responses for NuGet's API v3.

## Making Changes
Some very simple testing is set up. Testing requires Python 3.5 or higher.
To run tests:

1.  Clone the repo: `git clone git@github.com:dougthor42/nuget-api-v3-jsonschemas.git`
2.  Enter the cloned repo: `cd nuget-api-v3-jsonschemas`
3.  (Optional, but recommended) Create a virtual environment and activate it.
4.  Install the testing requirements: `pip install -r requirements-dev.txt`
5.  Run the tests: `pytest`
