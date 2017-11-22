# Dependências
O projeto roda em cima do Google App Engine com Python e utiliza MongoDB como banco. As bibliotecas utilizadas estão todas na subpasta lib/. Poderia ter deixado apenas um requirements.txt para ser utilizado com o pip -t lib mas resolvi deixar as bibliotecas aí por facilidade, já que é código apenas para avaliação.
As principais dependências são google-api-python-client, webapp2 (built-in do GAE) e pymongo.
Uma instância local do MongoDB foi utilizada e deve estar funcionando para que o código funcione. A configuração é a padrão.

## Importante
Também é necessário criar um projeto no Google Cloud Console e também a geração do CLIENT_ID e CLIENT_SECRET para configuração do OAuth2.

## Sobre o Tempo Utilizado
O tempo total utilizado foi de 6h. Dessas 6h, pelo menos 2h30 foram perdidas até descobrir/reescrever tudo de Flask para webapp2 -- bugs com OAuth2 e na lib Flask_GoogleLogin.

Do tempo líquido de desenvolvimento, pelo menos 2h foi perdida no front-end, que não é uma área que eu me considere apto a atuar em um bom nível.

Para quebrar o tempo por parte, como pedido, ficaria dessa forma:
Parte 1: 1h
Parte 2: 3h
Parte 3 e 4 (feitas juntas): 2h

Pensei em pesquisar como implementar a fila de prioridade e a indexação utilizando os serviços da AWS mas como nunca fiz isso e o tempo foi curto, deixei de lado. 
