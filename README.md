# Chronos
Gerenciador de tempo e atividades, sem muitas complicações e de setup rapido

# Setup Inicial

#### clone o repositorio
```
gh repo clone Perceu/chronos
```

#### Copie as variaveis de ambiente 
```
cp ./contrib/env-sample .env
```

#### Configure a segurança das sua aplicação no arquivo .env
```
nano .env
```

#### Suba o docker 
```
docker compose up -d
```

#### Rode as migrações
```
sh ./shell/migrate.sh
```

#### Crie o primeiro usuario
```
sh ./shell/add_user.sh
```

#### Agora basta acessar o sistema
[link local](http://localhost:8000)

