from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, text
import pandas as pd 
import sqlite3
from fastapi import FastAPI
import requests


#config da conexão com banco de dados
host = "127.0.0.1"
port = 3306
user = "root"
password = "Tricolor99"
banco_dados = "db_escola"


engine = create_engine("mysql+pymysql://root:Tricolor99@127.0.0.1:3306/db_escola")
# instanciar 
app = FastAPI()


#schema valida tanto a saida quanto a entrada de dados, ou seja, o que o usuario vai enviar para a api e o que a api vai retornar para o usuario
class Aluno(BaseModel):
    matricula:str
    nome_aluno:str
    # email:Optional[str] = None
    # endereco_id:Optional[int] = None

class MsgPost(BaseModel):
    mensagem:str

class EnderecoAPI(BaseModel):
    # id :  str
    cep : str
    # endereco : Optional[str] = None
    # bairro : Optional[str] = None
    # cidade : Optional[str] = None
    # estado : Optional[str] = None
    # regiao : Optional[str] = None




@app.get("/alunos/", response_model= List[Aluno])
def listar_alunos():
    query1 = "select * from tb_alunos"
    df_alunos=pd.read_sql(query1, con=engine)
    return df_alunos.to_dict(orient="records")


@app.get("/enderecos/")
def listar_enderecos():
    query2 = " select * from tb_enderecos "
    df_enderecos=pd.read_sql(query2, con=engine)
    return df_enderecos.to_dict(orient="records")

@app.get("/enderecos+alunos/")
def listar_enderecos_alunos():
    query3 = " select * from  vw_alunos_enderecos"
    df_enderecos_alunos=pd.read_sql(query3, con=engine)
    return df_enderecos_alunos.to_dict(orient="records")

@app.post("/cadastrar-endereco-cep/{cep}")
def cadastrar_endereco_viacep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    dados_endereco = resposta.json()

    if "erro" in dados_endereco:
        return {"mensagem": "Erro no CEP"}

    cep_formatado = dados_endereco.get("cep")

   
    query_verifica = text("SELECT id, cep FROM tb_enderecos WHERE cep = :cep")
    with engine.begin() as conn:
        endereco_existente = conn.execute(query_verifica, {"cep": cep_formatado}).fetchone()

        if endereco_existente:
            return {"mensagem": "CEP já cadastrado", "cep": cep_formatado}

        query_insert = text("""
            INSERT INTO tb_enderecos (cep, endereco, bairro, cidade, estado, regiao)
            VALUES (:cep, :endereco, :bairro, :cidade, :estado, :regiao)
        """)

        conn.execute(query_insert, {
            "cep": cep_formatado,
            "endereco": dados_endereco.get("logradouro"),
            "bairro": dados_endereco.get("bairro"),
            "cidade": dados_endereco.get("localidade"),
            "estado": dados_endereco.get("uf"),
            "regiao": dados_endereco.get("regiao")
        })

    return {"mensagem": "Endereço cadastrado com sucesso"}


@app.post("/cadastrar-endereco/")
def cadastrar_endereco(endereco: dict):
    cep = endereco.get("cep")

    if not cep:
        return {"mensagem": "O campo CEP é obrigatório"}

    query_verifica = text("SELECT id, cep FROM tb_enderecos WHERE cep = :cep")

    with engine.begin() as conn:
        endereco_existente = conn.execute(query_verifica, {"cep": cep}).fetchone()

        if endereco_existente:
            return {"mensagem": "CEP já cadastrado", "cep": cep}

        query_insert = text("""
            INSERT INTO tb_enderecos (cep, endereco, bairro, cidade, estado, regiao)
            VALUES (:cep, :endereco, :bairro, :cidade, :estado, :regiao)
        """)

        conn.execute(query_insert, {
            "cep": endereco.get("cep"),
            "endereco": endereco.get("endereco"),
            "bairro": endereco.get("bairro"),
            "cidade": endereco.get("cidade"),
            "estado": endereco.get("estado"),
            "regiao": endereco.get("regiao")
        })

    return {"mensagem": "Endereço cadastrado com sucesso"}


@app.post("/cadastrar-aluno/", response_model=MsgPost)
def cadastrar_alunos(aluno:dict):
   df = pd.DataFrame([aluno])
   df.to_sql("tb_alunos", engine, if_exists="append", index=False)
   return{"mensagem": "Aluno Cadastrado com sucesso"}

@app.put("/atualizar-alunos/{id}")
def atualizar_alunos(id:int, alunos:dict):
    with engine.begin()as conn:
        conn.execute(
            text(
            """
            update tb_alunos
            set matricula = :matricula,
            nome_aluno = :nome_aluno,
            email = :email,
            endereco_id = :endereco_id
            where id = :id
            """
            ), {"id":id, **alunos}
        )
    return{"message":"Aluno Atualizado"}


@app.delete("/deletar-alunos/{id}")
def deletar_alunos(id:int):
    with engine.begin() as conn:
        conn.execute(
            text(
            """
            delete from tb_alunos
            where id = :id
            """
            ), {"id":id }
        )
    return{"message":"Aluno Removido"}
























# query1 = "select * from tb_alunos"
# df_alunos=pd.read_sql(query1, con=engine)

# query2 = "select * from tb_enderecos"
# df_enderecos = pd.read_sql(query2, con=engine)

# # usando o merge do pandas
# pd.merge(df_alunos, df_enderecos, how="right", left_on="endereco_id", right_on="id")

# # usando join do sql

# query3 = """
# select a.matricula, a.nome_aluno, b.endereco, b.cep
# from tb_alunos a 
# right join tb_enderecos b
# on a.endereco_id = b.id;
# """
# pd.read_sql(query3, con=engine)



# #atraves da view
# query4 = "select * from vw_alunos_enderecos"
# df_merge = pd.read_sql(query4, con=engine)





# BASE_DIR = Path(__file__).parent.resolve() #falar o lugar que vai criar
# db_path = BASE_DIR / "meu_banco.db" #cria o banco de dados sqlite
# conn = sqlite3.connect(db_path)

# engine = create_engine (f'sqlite:///{db_path}')

# with engine.begin() as conn :
#     resultado = conn.execute(
#         text("""
#         select * from usuarios ;
#             """)
#     )

#     print(resultado)
#     for linha in resultado : 
#         print(linha)

# import pandas as pd

# df = pd.read_sql("select * from usuarios", con=engine)
# df

