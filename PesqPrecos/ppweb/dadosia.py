from ppweb.ext.database import db
from ppweb.models import Itenscontratos, Itens, ComprasContratos, Licitacao, Material, \
    Itensprecospraticados
from ppweb.utils import baixa_json_material


def busca_data(id):
    contrato = ComprasContratos.query.filter(id=id).first()
    if contrato is None:
        print('não achou contrato')
        return '1970-01-01'
    else:
        return contrato.data_assinatura


def busca_data_licitacao(uasg, modalidade, numero_aviso):
    print('entrei na busca da data licitacao')
    licitacao = Licitacao.query.filter_by(uasg=uasg, modalidade=modalidade,
                                          numero_aviso=numero_aviso).first()
    if licitacao is None:
        print('licitacao não encontrada')
        return '1970-01-01'
    else:
        return licitacao.data_abertura_proposta[:10]


def busca_material(catmat):
    material = Material.query.filter_by(codigo=catmat).first()
    if material is None:
        material = baixa_json_material(catmat)
        if material is None:
            print('não achei o material')
    return material


def atualiza_materiais():
    registros = Itens.query.all()
    i = 0
    n = len(registros)
    for item in registros:
        i = i + 1
        print('processando item ' + str(i) + ' de ' + str(n))
        busca_material(item.catmat_id)


def carrega_itens_contratos():
    try:
        # dfc=pd.read_sql(SQL,conn)
        catmat = 0
        itens = Itenscontratos.query.filter(tipo_id='Material').all()
        i = 0
        if i == 0:
            print('não achou')
        for itemc in itens:
            try:
                i = i + 1
                print('processando item de contratos ' + str(i) + ' de ' + str(len(itens)))
                gap_pos = itemc.catmatser_item_id.find(" ")
                catmatstr = itemc.catmatser_item_id[0:gap_pos]
                catmat = int(catmatstr)
                print(catmat)
                item = Itens.query.filter_by(id=itemc.id, licitacao_contrato=0).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = 0
                print(item.licitacao_contrato)
                item.id = itemc.id
                item.data = busca_data(itemc.contrato_id)
                item.catmat_id = catmat
                item.quantidade = itemc.quantidade
                item.valor_unitario = itemc.valor_unitario
                item.valor_total = itemc.valor_total
                if itemc.valor_unitario is None:
                    if itemc.valor_total is None:
                        continue
                    else:
                        item.valor_unitario = itemc.valor_total / float(itemc.quantidade)
                else:
                    item.valor_unitario = itemc.valor_unitario

                if exists:
                    item.verified = True
                else:
                    db.session.add(item)
                db.session.commit()
            except Exception as excep:
                print('Erro com o material = ' + str(catmat) + str(excep.__cause__))
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def carrega_itens_licitacoes():
    print('entrei itens de licitações')
    try:
        itens = Itensprecospraticados.query.filter_by(codigo_item_servico=0).all()
        i = 0
        print('Número de licitações=' + str(len(itens)))
        for iteml in itens:
            try:
                i = i + 1
                print('processando item de licitação ' + str(i) + ' de ' + str(len(itens)))
                id = int(iteml.id_licitacao)
                item = Itens.query.filter_by(id=id,
                                             licitacao_contrato=iteml.numero_item_licitacao).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = iteml.numero_item_licitacao
                item.id = id
                item.data = busca_data_licitacao(iteml.uasg, iteml.modalidade, iteml.numero_aviso)
                print(item.data)
                item.catmat_id = iteml.codigo_item_material
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
                item.uf_uasg = 'UF'
                if exists:
                    item.verified = True
                else:
                    db.session.add(item)
                db.session.commit()
            except Exception as ex:
                print('Erro no item = ' + str(i))
                print(ex.args)
                print(ex.__traceback__)
                break
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))
        print(excecao.args)
        print(excecao.__traceback__)
