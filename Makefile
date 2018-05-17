.PHONY: serve example_jieba clean

fetch: env
	fab fetch

console: env
	fab console

env: requirements.txt
	fab setup

clean:
	@rm -rf *.egg-info
	@rm -rf env
	@rm -rf build
	@rm -rf dist
	@rm -rf *.pyc
