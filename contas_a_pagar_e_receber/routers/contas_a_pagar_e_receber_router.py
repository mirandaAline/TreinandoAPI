from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import ContaPagarRecber
from shared.dependencies import get_db  



router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    
class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str
    

@router.get("", response_model=list[ContaPagarReceberResponse])
def listar_contas():
    return [
        ContaPagarReceberResponse(
            id=1,
            descricao="Aluguel",
            valor=1000,
            tipo="Pagar"
        ),
        ContaPagarReceberResponse(
            id=2,
            descricao="Salario",
            valor=5000,
            tipo="Receber"
        ),
    ]
    
@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_a_pagar_e_receber_request: ContaPagarReceberRequest, 
                db: Session = Depends(get_db))-> ContaPagarReceberResponse :
    conta_a_pagar_e_receber = ContaPagarRecber(
        **conta_a_pagar_e_receber_request.dict()
    )
    
    db.add(conta_a_pagar_e_receber)
    db.commit()
    db.refresh(nova_conta)
    return nova_conta
