.PHONY: tag

tag:
	@VERSION="$$(grep -m1 -E '^[[:space:]]*version[[:space:]]*=' Cargo.toml | sed -E 's/^[[:space:]]*version[[:space:]]*=[[:space:]]*"([^"]+)"[[:space:]]*$$/v\1/')"; \
	if [ -z "$$VERSION" ] || [ "$$VERSION" = "v" ]; then \
		echo "Erro: não foi possível ler a versão do Cargo.toml"; \
		exit 1; \
	fi; \
	if ! echo "$$VERSION" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$$'; then \
		echo "Erro: versão do Cargo.toml deve estar no formato semver (ex: 1.2.3)"; \
		exit 1; \
	fi; \
	LAST_TAG="$$(git tag --list 'v[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -n 1)"; \
	if [ -n "$$LAST_TAG" ] && [ "$$(printf '%s\n%s\n' "$$VERSION" "$$LAST_TAG" | sort -V | head -n 1)" = "$$VERSION" ]; then \
		echo "Erro: versão ($$VERSION) deve ser maior que a última tag ($$LAST_TAG)"; \
		exit 1; \
	fi; \
	git tag "$$VERSION"; \
	git push origin "$$VERSION"; \
	echo "Tag $$VERSION criada e enviada para o GitHub."
