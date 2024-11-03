Para Executar o programa digite no terminal:

- INICIE O DOCKER:
- docker-compose up --build
- Depois que aparecer isso no terminal:
- ![image](https://github.com/user-attachments/assets/010aaec2-8bd5-417b-a0b5-f204f379d282)

- Entre no docker e clique no link:
- ![image](https://github.com/user-attachments/assets/bb9f8548-3bad-4526-8700-43ea9e088aa4)

- Preencha todos os dados e clique em "gerar certificado"
- Logo depois verifique se o certificado foi salvo na pasta "Certificaados"

- Caso queira mandar pelo postman:
- No PostMan coloque o link: http://127.0.0.1:5000/emitir_certificado
- Coloque o seguinte no "BODY":
{
  "nome": "PostMan",
  "cpf": "123.456.789-00",
  "nacionalidade": "Brasileiro",
  "estado": "SP",
  "curso": "Docker Essentials",
  "data": "2024-11-01"
}

- Selecione como RAW e mude para POST
- Clique em enviar
- Se aparecer "OK" de tudo certo

- Para executar localmente:
- Digite python app.py
- e cliqe no link gerado
- (obs: para funcionar tem que ter todos os Requirements instalados)
