docker build -t painel-aguas-limpas-db .
docker network create painel-aguas-limpas || true
docker run --name painel-aguas-limpas-db --hostname painel-aguas-limpas-db -e POSTGRES_USER=f01 -e POSTGRES_PASSWORD=f01 -e POSTGRES_DB=f01_dev --network painel-aguas-limpas -v postgres_data:/var/lib/postgresql/data/ -p 60107:5432 -d painel-aguas-limpas-db