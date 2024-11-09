from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def teste_deve_listar_contas_a_pagar_e_receber():
    reponse = client.get('/contas-a-pagar-e-receber')
    
    assert reponse.status_code ==200

    
    assert reponse.json() == [ 
        {'descricao': 'Aluguel', 'id': 1, 'tipo': 'Pagar', 'valor': '1000'},
        {'id': 2, 'descricao': 'Salario', 'valor': '5000', 'tipo': 'Receber'}
    ]
    
def teste_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {
        "descricao": "Boleto",
        "valor": 333,
        "tipo": "Pagar"
    }
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 3
    
    response = client.post('/contas-a-pagar-e-receber', json=nova_conta)

    
    assert response.status_code == 201