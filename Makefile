NAME:=chbndhrnns/vuepress2pdf

reqs:
	pipenv lock -r > requirements.txt

build: reqs
	docker build --rm=true -t $(NAME) .