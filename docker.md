# Install instructions

To install the environment required to run these scripts:

	apt-get update && apt-get upgrade -y
	apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info git pandoc wget fonts-roboto -y
	pip3 install WeasyPrint pypandoc pyyaml pandas matplotlib unidecode readability spacy subprocess bs4 jq aylien-apiclient
	python -m spacy download en_core_web_sm
