.PHONY: run

include .env
export

run:
	uvicorn app.main:app