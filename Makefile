.PHONY:
.SILENT:

init:
	pip install -r requirements.txt

run-mongo:
	docker run -d \
  	--name mongodb \
  	--network tgbotnet \
  	-p 27017:27017 \
  	-e MONGO_INITDB_ROOT_USERNAME=admin \
  	-e MONGO_INITDB_ROOT_PASSWORD=qwerty123456 \
  	mongo

run:
	python main.py