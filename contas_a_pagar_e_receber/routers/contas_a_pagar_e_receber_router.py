from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import ContaPagarReceber
from shared.dependencies import get_db  



router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    
    class Config:
        orm_mode = True 
    
class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str
    

@router.get("", response_model=list[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db))-> list[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()
    
    
@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_request: ContaPagarReceberRequest, 
                db: Session = Depends(get_db))-> ContaPagarReceberResponse :
    nova_conta = ContaPagarReceber(
        **conta_request.dict()
    )
    
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    return nova_conta


@router.put("/{conta_id}", response_model= ContaPagarReceberResponse, status_code =200)
def atualizar_conta(conta_id: int, conta_request: ContaPagarReceberRequest, db: Session = Depends(get_db))-> ContaPagarReceberResponse:
    conta = db.query(ContaPagarReceber).filter(ContaPagarReceber.id == conta_id).first()
    
    if not conta:
        raise HTTPException(status_code=404, detail= "Conta não encontrada")
    
    for key, value in conta_request.dict().items():
        setattr(conta, key, value)
        
    db.commit()
    db.refresh(conta)
    
    return conta

@router.delete("/{conta_id}", status_code=204)
def deletar_conta(conta_id: int, db: Session = Depends(get_db)):
    conta = db.query(ContaPagarReceber).filter(ContaPagarReceber.id == conta_id).first()
    
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    db.delete(conta)
    db.commit()
    return {"message": "Conta deletada com sucesso"}