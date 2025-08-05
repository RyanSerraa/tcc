compose-up:
	docker compose -f docker-compose.yml up -d --build
compose-down:
	docker compose -f docker-compose.yml -v down
exec-llm:
	docker compose -f docker-compose.yml exec -it llm bash
exec-ollama:
	docker compose -f docker-compose.yml exec -it ollama bash
ollama-pull:
	ollama pull deepseek-r1:7b
llm-install:
	pip install -r requirements.txt

llm-run:
	streamlit run text_to_sql.py
