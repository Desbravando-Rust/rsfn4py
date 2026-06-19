.PHONY: tag

tag:
	@if [ -z "$(VERSION)" ]; then \
		echo "Uso: make tag VERSION=vX.Y.Z"; \
		exit 1; \
	fi
	@if ! echo "$(VERSION)" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$$'; then \
		echo "Erro: VERSION deve estar no formato semver com prefixo v (ex: v1.2.3)"; \
		exit 1; \
	fi
	@LAST_TAG="$$(git tag --list 'v[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -n 1)"; \
	if [ -n "$$LAST_TAG" ] && [ "$$(printf '%s\n%s\n' "$(VERSION)" "$$LAST_TAG" | sort -V | head -n 1)" = "$(VERSION)" ]; then \
		echo "Erro: VERSION ($(VERSION)) deve ser maior que a última tag ($$LAST_TAG)"; \
		exit 1; \
	fi
	@git tag "$(VERSION)"
	@git push origin "$(VERSION)"
	@echo "Tag $(VERSION) criada e enviada para o GitHub."
