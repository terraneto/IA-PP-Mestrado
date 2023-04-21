from sqlalchemy.sql.elements import Null

from ppweb.ext.database import db
from ppweb.models import Itenscontratos, Itens, ComprasContratos, Licitacao, Material, \
    Itensprecospraticados
from ppweb.utils import baixa_json_material


def busca_data(id):
    contrato = ComprasContratos.query.filter(ComprasContratos.id == id).first()
    if contrato is None:
        print('não achou contrato')
        return None
    else:
        return contrato.data_assinatura


def busca_data_licitacao(uasg, modalidade, numero_aviso):
    licitacao = Licitacao.query.filter(Licitacao.uasg == uasg, Licitacao.modalidade == modalidade,
                                       Licitacao.numero_aviso == numero_aviso).first()
    if licitacao is None:
        return None
    else:
        return licitacao.data_abertura_proposta[:10]


def busca_material(catmat):
    material = Material.query.filter(Material.codigo == catmat).first()
    if material is None:
        material = baixa_json_material(catmat)
    return material


def carrega_itens_contratos():
    try:
        # dfc=pd.read_sql(SQL,conn)
        itens = Itenscontratos.query.filter(Itenscontratos.tipo_id == 'Material').all()
        i = 0
        for itemc in itens:
            try:
                i = i + 1
                print('processando item de contratos ' + str(i) + ' de ' + str(len(itens)))
                gap_pos = itemc.catmatser_item_id.find(" ")
                catmatstr = itemc.catmatser_item_id[0:gap_pos]
                catmat = int(catmatstr)
                material = busca_material(catmat)
                item = Itens.query.filter(Itens.id == itemc.id, Itens.licitacao_contrato == 0).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = 0
                item.id = itemc.id
                item.data = busca_data(itemc.contrato_id)
                item.catmat_id = catmat
                if material is not None:
                    item.pdm_id = material.id_pdm
                    item.grupo_id = material.id_grupo
                    item.classe_id = material.id_classe
                item.quantidade = itemc.quantidade
                item.valor_unitario = itemc.valor_unitario
                item.valor_total = itemc.valor_total
                if exists:
                    item.verified = True
                else:
                    db.session.add(item)
                db.session.commit()
            except Exception as excep:
                print('Erro com o material = ' + str(catmat) + excep.__cause__)
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def carrega_itens_licitacoes():
    print('entrei itens de licitações')
    try:
        itens = Itensprecospraticados.query.filter(
            Itensprecospraticados.codigo_item_servico == 0).all()
        i = 0
        print('Número de licitações=' + str(len(itens)))
        for iteml in itens:
            try:
                i = i + 1
                print('processando item de licitação ' + str(i) + ' de ' + str(len(itens)))
                if i < 150744:
                    continue
                id = int(iteml.id_licitacao)
                item = Itens.query.filter(Itens.id == id,
                                          Itens.licitacao_contrato == iteml.numero_item_licitacao).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = iteml.numero_item_licitacao
                item.id = id
                item.data = busca_data_licitacao(iteml.uasg, iteml.modalidade, iteml.numero_aviso)
                item.catmat_id = iteml.codigo_item_material
                material = busca_material(iteml.codigo_item_material)
                if material is not None:
                    item.pdm_id = material.id_pdm
                    item.grupo_id = material.id_grupo
                    item.classe_id = material.id_classe
                item.quantidade = iteml.quantidade
                item.unidade = iteml.unidade
                if iteml.valor_unitario is None:
                    if iteml.valor_total is None:
                        continue
                    else:
                        item.valor_unitario = iteml.valor_total / float(iteml.quantidade)
                else:
                    item.valor_unitario = iteml.valor_unitario
                item.valor_total = iteml.valor_total
                if exists:
                    item.verified = True
                else:
                    db.session.add(item)
                db.session.commit()
            except Exception as ex:
                print('Erro no item = ' + str(i))
                print(ex.args)
                print(ex.__traceback__)
                continue
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        print(excecao.args)
        print(excecao.__traceback__)
