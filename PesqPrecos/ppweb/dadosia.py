from ppweb.ext.database import db
from ppweb.geocode import calcula_distancia_circunferencia
from ppweb.models import Itenscontratos, Itens, ComprasContratos, Licitacao, Material, \
    Itensprecospraticados, Fornecedor, Uasg


def busca_municipio_fornecedor_pj(cnpj_fornecedor):
    fornecedor = Fornecedor.query.filter_by(cnpj=cnpj_fornecedor).first()
    idmunicipio = 0
    if fornecedor is not None:
        idmunicipio = fornecedor.id_municipio
    return idmunicipio


def busca_municipio_fornecedor_pf(nome_fornecedor):
    fornecedor = Fornecedor.query.filter_by(nome=nome_fornecedor).first()
    idmunicipio = 0
    if fornecedor is not None:
        idmunicipio = fornecedor.id_municipio
    return idmunicipio


def carrega_itens_contratos():
    try:
        itens = db.session.query(Itenscontratos, ComprasContratos, Uasg) \
            .filter((Itenscontratos.tipo_id == 'Material') & ((
                      (Itenscontratos.valor_unitario > 0) | (
                      Itenscontratos.valor_total > 0))
              & ((Itenscontratos.valor_unitario is not None
                  ) | (Itenscontratos.valor_total is not None))) & (
                            Itenscontratos.catmatser_item_id is not None)
                    ) \
            .join(ComprasContratos, Itenscontratos.contrato_id == ComprasContratos.id) \
            .join(Uasg, ComprasContratos.unidade_codigo == Uasg.id) \
            .all()
        i = 0
        for itemc in itens:
            try:
                i = i + 1
                print('processando item de contratos ' + str(i) + ' de ' + str(len(itens)))
                try:
                    gap_pos = itemc[0].catmatser_item_id.find(" ")
                    catmatstr = itemc[0].catmatser_item_id[0:gap_pos]
                    catmat = int(catmatstr)
                except Exception as excep:
                    print('Erro com o material = ' + str(catmat) + str(excep.__cause__))
                    catmat = 0
                item = Itens.query.filter_by(id=itemc[0].id, licitacao_contrato=0).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = 0
                item.id = itemc[0].id
                item.data = itemc[1].data_assinatura
                item.catmat_id = catmat
                item.quantidade = itemc[0].quantidade
                item.valor_unitario = itemc[0].valor_unitario
                item.valor_total = itemc[0].valor_total
                if itemc[0].valor_unitario is None:
                    if itemc[0].valor_total is None:
                        continue
                    else:
                        item.valor_unitario = itemc[0].valor_total / float(itemc[0].quantidade)
                else:
                    item.valor_unitario = itemc[0].valor_unitario
                try:
                    idcidade1 = int(itemc[2].id_municipio)
                    item.municipio_uasg = idcidade1
                    if itemc[1].fornecedor_tipo == 'JURIDICA':
                        idf = itemc[1].fornecedor_cnpj_cpf_idgener
                        cnpj_fornecedor = str(idf[0:2] + idf[3:6] + idf[7:10] + idf[11:15] + idf[16:18])
                        idcidade2 = busca_municipio_fornecedor_pj(cnpj_fornecedor)
                    else:
                        idcidade2 = busca_municipio_fornecedor_pf(itemc[1].fornecedor_nome)
                    item.municipio_fornecedor = idcidade2
                    if idcidade1 == 0 or idcidade2 == 0:
                        distanciacidades = 0.0
                    else:
                        distanciacidades = calcula_distancia_circunferencia(idcidade1, idcidade2)
                    item.distancia_uasg_fornecedor = distanciacidades
                except:
                    print('Erro com o calculo da distância do registro = ' + str(i))
                item.unidade = ' '
                if exists:
                    item.verified = True
                else:
                    db.session.add(item)
                db.session.commit()
            except Exception as excep:
                print('Erro com o registro = ' + str(i))
    except Exception as excecao:
        print("Erro na gravação no banco " + str(excecao.__cause__))


def carrega_itens_licitacoes():
    try:
        itens = db.session.query(Itensprecospraticados, Licitacao, Uasg) \
            .filter((Itensprecospraticados.codigo_item_servico == 0) & ((
                            (
                                        Itensprecospraticados.valor_unitario > 0) | (
                                    Itensprecospraticados.valor_total > 0))
                    & ((
                               Itensprecospraticados.valor_unitario is not None
                       ) | (
                                   Itensprecospraticados.valor_total is not None)))) \
            .join(Licitacao, int(Itensprecospraticados.id_licitacao) == int(Licitacao.identificador)) \
            .join(Uasg, Itensprecospraticados.uasg == Uasg.id) \
            .all()
        i = 0
        print('Número de licitações=' + str(len(itens)))
        for iteml in itens:
            try:
                i = i + 1
                print('processando item de licitação ' + str(i) + ' de ' + str(len(itens)))
                id = int(iteml[0].id_licitacao)
                item = Itens.query.filter_by(id=id,
                                             licitacao_contrato=iteml[0].numero_item_licitacao).first()
                if item is None:
                    exists = False
                    item = Itens()
                else:
                    exists = True
                item.licitacao_contrato = iteml[0].numero_item_licitacao
                item.id = id
                item.data = iteml[1].data_publicacao
                item.catmat_id = iteml[0].codigo_item_material
                item.quantidade = iteml[0].quantidade
                item.unidade = iteml[0].unidade
                if iteml[0].valor_unitario is None:
                    if iteml[0].valor_total is None:
                        continue
                    else:
                        item.valor_unitario = iteml[0].valor_total / float(iteml[0].quantidade)
                else:
                    item.valor_unitario = iteml[0].valor_unitario
                item.valor_total = iteml[0].valor_total
                idcidade1 = int(iteml[2].id_municipio)
                item.municipio_uasg = idcidade1
                idcidade2 = int(busca_municipio_fornecedor_pj(iteml[0].cnpj_fornecedor))
                item.municipio_fornecedor = idcidade2
                distanciacidades = calcula_distancia_circunferencia(idcidade1, idcidade2)
                item.distancia_uasg_fornecedor = distanciacidades
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


def corrige_calculo_distancia():
    try:
        itens = Itens.query.filter((Itens.municipio_uasg == 0) | (Itens.municipio_fornecedor == 0) | (
                Itens.distancia_uasg_fornecedor == 0)).all()
        i = 0
        print('Número de itens a corrigir=' + str(len(itens)))
        for item in itens:
            i = i + 1
            print('processando item  ' + str(i) + ' de ' + str(len(itens)))
            try:
                if item.licitacao_contrato == 0:
                    itenscontratos = Itenscontratos.query.filter_by(id=item.id).first()
                    contrato = ComprasContratos.query.filter_by(id=itenscontratos.contrato_id).first()
                    if contrato is None:
                        item.municipio_uasg = 0
                        item.municipio_fornecedor = 0
                        item.distancia_uasg_fornecedor = 0.0
                    else:
                        idcidade1 = item.municipio_uasg
                        idcidade2 = item.municipio_fornecedor
                        if item.municipio_uasg == 0:
                            try:
                                uasg = Uasg.query.filter_by(id=contrato.unidade_codigo).first()
                                print(uasg)
                                item.municipio_uasg = uasg.id_municipio
                                idcidade1 = uasg.id_municipio
                            except:
                                print('Erro da busca da uasg')
                            item.municipio_uasg=idcidade1
                        if item.municipio_fornecedor == 0:
                            try:
                                if contrato.fornecedor_tipo == 'JURIDICA':
                                    idf = contrato.fornecedor_cnpj_cpf_idgener
                                    cnpj_fornecedor = str(idf[0:2] + idf[3:6] + idf[7:10] + idf[11:15] + idf[16:18])
                                    idcidade2 = busca_municipio_fornecedor_pj(cnpj_fornecedor)
                                else:
                                    idcidade2 = busca_municipio_fornecedor_pf(contrato.fornecedor_nome)
                            except:
                                print('Erro na busca do fornecedor')
                            item.municipio_fornecedor=idcidade2
                        if idcidade1 != 0 and idcidade2 != 0 and idcidade1 != idcidade2:
                            distanciacidades = calcula_distancia_circunferencia(idcidade1, idcidade2)
                        else:
                            distanciacidades = 0.0
                        item.distancia_uasg_fornecedor = distanciacidades
                else:
                    print('item de licitacao')
                    idlicitacao = str(item.id).zfill(17)
                    itemlicitacao = Itensprecospraticados.query.filter((
                        (Itensprecospraticados.id_licitacao == idlicitacao)
                        & (Itensprecospraticados.numero_item_licitacao == item.licitacao_contrato))).first()
                    print(itemlicitacao)
                    print(idlicitacao)
                    print(item.licitacao_contrato)
                    idcidade1 = item.municipio_uasg
                    idcidade2 = item.municipio_fornecedor
                    print(idcidade1,idcidade2)
                    if item.municipio_uasg == 0:
                        try:
                            uasg = Uasg.query.filter_by(id=itemlicitacao.uasg).first()
                            item.municipio_uasg = uasg.id_municipio
                            idcidade1 = uasg.id_municipio
                        except:
                            print('Erro da busca da uasg')
                        item.municipio_uasg = idcidade1
                    if item.municipio_fornecedor == 0:
                        try:
                            idcidade2 = busca_municipio_fornecedor_pj(itemlicitacao.cnpj_fornecedor)
                        except:
                            print('Erro na busca do fornecedor')
                        item.municipio_fornecedor = idcidade2
                    if idcidade1 != 0 and idcidade2 != 0 and idcidade1 != idcidade2:
                        distanciacidades = calcula_distancia_circunferencia(idcidade1, idcidade2)
                    else:
                        distanciacidades = 0.0
                    item.distancia_uasg_fornecedor = distanciacidades
                item.verified = True
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
