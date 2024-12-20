Para Executar a API siga os passos abaixo:

- Digite no terminal:
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
<br>
{
<br>
  "nome": "PostMan",  
  <br>
  "cpf": "123.456.789-00",
  <br>
  "nacionalidade": "Brasileiro",
  <br>
  "estado": "SP",
  <br>
  "curso": "Docker Essentials",
  <br>
  "data": "2024-11-01"
    <br>
}
<br>
Preencha os campos e depois clique em "Gerar PDF"

![image](https://github.com/user-attachments/assets/ef1cddb4-5714-402d-bc4e-9f964c87f0bf)

<br>
 link do curl:
<br>
  curl --location 'http://127.0.0.1:5000/emitir_certificado' \
  <br>
--header 'Content-Type: application/json' \
  <br>
--data ' { "nome": "Teste no postMan",
  <br> 
    "cpf": "123.456.789-00",
  <br> 
    "nacionalidade": "Brasileiro",
  <br>
    "estado": "SP",
  <br>
    "curso": "Docker Essentials",
  <br>
    "data": "2024-11-01"
  <br>
 }'
<br>
</br>
- Selecione como RAW e mude para POST
- Clique em enviar
- Se aparecer "OK" de tudo certo
<br>
- Para executar localmente:
- Digite: python app.py
- e cliqe no link gerado
- (obs: para funcionar tem que ter todos os Requirements instalados)
