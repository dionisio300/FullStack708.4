import boto3
from flask import *

s3 = boto3.client(
    "s3",
    aws_access_key_id = "",
    aws_secret_access_key = "",
    region_name = "us-east-1"
)

app = Flask(__name__)



@app.route("/upload", methods=["GET", "POST"])
def upload():
    print('Acessou o upload')

    if request.method == "GET":
        return render_template('index.html')
    
    if request.method == "POST":
        
        arquivo = request.files.get('imagem')
        print(arquivo)
        if arquivo:
            caminho = 'uploads/'+arquivo.filename
            print(caminho)

            s3.upload_fileobj(arquivo,'python-youth-708-04',caminho)

            url = f"https://aplicacao-python-upload.s3.amazonaws.com/{caminho}"
            print("URL:",url)
            return render_template('index.html',url=url)

        return render_template('index.html')


@app.route("/listar")
def listar():

    resposta = s3.list_objects_v2(Bucket='python-youth-708-04')

    urls = []

    print(resposta['Contents'])

    for nome in resposta['Contents']:
        url = f'https://python-youth-708-04.s3.amazonaws.com/{nome['Key']}'
        urls.append(url)
        
        partes = url.split('/')
        print(partes)
    
    
        

    return render_template('index.html',urls=urls)

if __name__ == "__main__":
    app.run(debug=True)