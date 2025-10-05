compose-up:
	docker compose -f docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f docker/docker-compose.yml down -v

exec-llm:
	docker compose -f docker/docker-compose.yml exec llm bash

llm-install:
	pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

llm-run:
	PYTHONPATH=. streamlit run src/main.py
