from datetime import date

from django.core.management.base import BaseCommand

from apps.accounts.models import Paroquia, Usuario
from apps.atendimentos.models import Atendimento, ItemAtendimento
from apps.bazar.models import (
    CatalogoBazar, EntradaBazar, EmpresaParceira,
    ItemEntradaBazar, ItemEstoqueBazar, Venda,
)
from apps.brecho.models import BrechoEvento, VendaBrecho
from apps.cestas.models import CestaPronta, EntregaCesta, ItemMontagem
from apps.doacoes.models import Doacao, ItemDoacao
from apps.estoque.models import ItemEstoque, ProdutoCatalogo
from apps.familias.models import Dependente, Familia
from apps.financeiro.models import MovimentacaoFinanceira


class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstração cobrindo todos os módulos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\nIniciando seed de demonstração...'))

        # ── 1. Paróquias ──────────────────────────────────────────────────────
        parq_sj = Paroquia.objects.create(
            nome='São José',
            cidade='Caxias do Sul',
            bairro='Centro',
            endereco='Rua Sinimbu, 1500',
            telefone='(54) 3200-0001',
            email='paroquia.saojose@caritas.org.br',
        )
        parq_nsa = Paroquia.objects.create(
            nome='Nossa Senhora Aparecida',
            cidade='Caxias do Sul',
            bairro='Vila Cristina',
            endereco='Av. Flores da Cunha, 2800',
            telefone='(54) 3300-0002',
            email='paroquia.nsa@caritas.org.br',
        )
        self.stdout.write('  ✓ Paróquias (2)')

        # ── 2. Usuários ────────────────────────────────────────────────────────
        # admin: get_or_create porque build.sh o cria antes com DJANGO_SUPERUSER_PASSWORD.
        # Não alteramos a senha para preservar a credencial definida no Render.
        admin, created = Usuario.objects.get_or_create(username='admin')
        admin.first_name = 'Administrador'
        admin.last_name = 'Sistema'
        admin.email = 'admin@caritas.org.br'
        admin.perfil = 'administrador'
        admin.paroquia = None
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        if created:
            admin.set_password('senha123')
        admin.save()

        def make_user(username, first, last, email, perfil, paroquia):
            u = Usuario.objects.create(
                username=username, first_name=first, last_name=last,
                email=email, perfil=perfil, paroquia=paroquia, is_active=True,
            )
            u.set_password('senha123')
            u.save()
            return u

        coord_sj    = make_user('coord_sj',    'Maria',  'Coordenadora', 'coord.sj@caritas.org.br',    'coordenador',     parq_sj)
        vol_sj      = make_user('vol_sj',      'João',   'Voluntário',   'vol.sj@caritas.org.br',      'voluntario',      parq_sj)
        coord_nsa   = make_user('coord_nsa',   'Ana',    'Coordenadora', 'coord.nsa@caritas.org.br',   'coordenador',     parq_nsa)
        coord_bazar = make_user('coord_bazar', 'Lúcia',  'Bazar',        'coord.bazar@caritas.org.br', 'coordenador_bazar', None)
        self.stdout.write('  ✓ Usuários (5) — senha: senha123')

        # ── 3. Catálogo de Produtos ────────────────────────────────────────────
        def prod(nome, cat, **kw):
            return ProdutoCatalogo.objects.create(
                nome=nome, categoria=cat, paroquia=parq_sj, **kw
            )

        c_arroz    = prod('Arroz',       'alimento')
        c_feijao   = prod('Feijão',      'alimento')
        c_oleo     = prod('Óleo De Soja','alimento')
        c_macarrao = prod('Macarrão',    'alimento')
        c_acucar   = prod('Açúcar',      'alimento')
        c_sal      = prod('Sal',         'alimento')
        c_leite    = prod('Leite Em Pó', 'alimento')
        c_camisa   = prod('Camisa',  'roupa',   genero='masculino', tamanho='m')
        c_calca    = prod('Calça',   'roupa',   genero='feminino',  tamanho='m')
        c_blusa    = prod('Blusa',   'roupa',   genero='infantil',  tamanho='p')
        c_tenis    = prod('Tênis',   'calcado', tipo_calcado='tenis',    tamanho_calcado='40')
        c_sandalia = prod('Sandália','calcado', tipo_calcado='sandalia', tamanho_calcado='37')
        prod('Chinelo', 'calcado', tipo_calcado='chinelo', tamanho_calcado='38')
        self.stdout.write('  ✓ Catálogo de produtos (13)')

        # ── 4. Estoque ─────────────────────────────────────────────────────────
        # Quantidades FINAIS — já descontadas: 10 de cada alimento (cestas montagem),
        # 2 camisas (atendimento) + 5 camisas e 3 calças (brechó vendas).
        def item_est(produto, qtd, unid, validade=None):
            i = ItemEstoque(
                paroquia=parq_sj, produto=produto,
                quantidade=qtd, unidade=unid, validade=validade,
                registrado_por=coord_sj,
            )
            i.save()
            return i

        e_arroz    = item_est(c_arroz,    40, 'kg',      date(2027, 1, 15))
        e_feijao   = item_est(c_feijao,   30, 'kg',      date(2026, 12, 10))
        e_oleo     = item_est(c_oleo,     20, 'unidade', date(2026, 10, 1))
        e_macarrao = item_est(c_macarrao, 50, 'pacote',  date(2026, 11, 20))
        e_acucar   = item_est(c_acucar,   25, 'kg',      date(2027, 3, 1))
        e_leite    = item_est(c_leite,    20, 'lata',    date(2026, 6, 28))  # vence em breve
        e_sal      = item_est(c_sal,      15, 'kg',      date(2026, 6, 10))  # já vencido
        e_camisa   = item_est(c_camisa,    5, 'unidade')
        e_calca    = item_est(c_calca,     5, 'unidade')
        item_est(c_tenis, 5, 'par')
        self.stdout.write('  ✓ Estoque (10 itens — 1 vencendo em breve, 1 vencido)')

        # ── 5. Famílias + Dependentes ──────────────────────────────────────────
        def familia(resp, cpf, possui_cpf, mae, pai, nasc, nac, end, tel,
                    esc, ocup, sit, renda, bolsa, benef, qtd_p, qtd_c, deps):
            f = Familia.objects.create(
                responsavel_nome=resp, cpf=cpf, possui_cpf=possui_cpf,
                nome_mae=mae, nome_pai=pai, data_nascimento=nasc,
                nacionalidade=nac, endereco=end, telefone=tel,
                escolaridade=esc, ocupacao=ocup,
                situacao_vulnerabilidade=sit, renda_familiar=renda,
                bolsa_familia=bolsa, valor_beneficio=benef,
                qtd_pessoas=qtd_p, qtd_criancas=qtd_c,
                paroquia_responsavel=parq_sj, criado_por=coord_sj,
            )
            for nome, idade, genero in deps:
                Dependente.objects.create(familia=f, nome=nome, idade=idade, genero=genero)
            return f

        f_maria = familia(
            'Maria Silva', '111.222.333-44', True,
            'Joana Silva', 'Pedro Silva', date(1985, 3, 12),
            'Brasileira', 'Rua das Acácias, 320 — Caxias do Sul/RS', '(54) 99900-1111',
            'medio_completo', 'Desempregada',
            'Mãe solo com três filhos menores, desempregada há 8 meses.',
            400.00, True, 200.00, 4, 3,
            [('Lucas Silva', 8, 'masculino'), ('Beatriz Silva', 5, 'feminino'), ('Pedro Silva', 2, 'masculino')],
        )
        f_joao = familia(
            'João Pereira', '222.333.444-55', True,
            'Rosa Pereira', 'Antônio Pereira', date(1978, 7, 22),
            'Brasileira', 'Av. Júlio de Castilhos, 890 — Caxias do Sul/RS', '(54) 99911-2222',
            'fundamental_completo', 'Trabalho informal (serviços gerais)',
            'Renda instável, trabalha de bico sem carteira assinada.',
            900.00, False, None, 2, 0,
            [('Carla Pereira', 30, 'feminino')],
        )
        f_ana = familia(
            'Ana Souza', '333.444.555-66', True,
            'Helena Souza', 'José Souza', date(1968, 11, 5),
            'Brasileira', 'Rua Bento Gonçalves, 440 — Caxias do Sul/RS', '(54) 99922-3333',
            'medio_incompleto', 'Cuidadora doméstica (informal)',
            'Viúva, cuida de mãe idosa com Alzheimer sem apoio familiar.',
            600.00, True, 300.00, 3, 0,
            [('Conceição Souza', 78, 'feminino'), ('Rafael Souza', 16, 'masculino')],
        )
        f_carlos = familia(
            'Carlos Oliveira', None, False,
            'Lucia Oliveira', 'Miguel Oliveira', date(1990, 5, 18),
            'Venezuelana', 'Rua Ernesto Alves, 150 — Caxias do Sul/RS', '(54) 99933-4444',
            'medio_completo', '',
            'Refugiado venezuelano sem documentação completa. Sem acesso a benefícios.',
            300.00, False, None, 5, 2,
            [('Lucia Oliveira', 28, 'feminino'), ('Miguel Oliveira', 6, 'masculino'), ('Sofia Oliveira', 4, 'feminino')],
        )
        f_fernanda = familia(
            'Fernanda Lima', '555.666.777-88', True,
            'Teresa Lima', 'Roberto Lima', date(1982, 9, 30),
            'Brasileira', 'Rua Garibaldi, 770 — Caxias do Sul/RS', '(54) 99944-5555',
            'superior', 'Auxiliar administrativo (parcial)',
            'Portadora de deficiência física (cadeirante). Necessita de apoio para acessibilidade.',
            750.00, True, 412.00, 3, 2,
            [('Mateus Lima', 14, 'masculino'), ('Isabela Lima', 9, 'feminino')],
        )
        self.stdout.write('  ✓ Famílias (5) + Dependentes (11)')

        # ── 6. Doações ─────────────────────────────────────────────────────────
        d1 = Doacao.objects.create(
            doador='Supermercado BomPreço', data=date(2026, 5, 10),
            descricao='Doação de alimentos para a campanha do inverno.',
            paroquia=parq_sj, registrado_por=coord_sj,
        )
        ItemDoacao.objects.create(doacao=d1, produto=c_arroz,    quantidade=20, unidade='kg',      data_validade=date(2027, 1, 15))
        ItemDoacao.objects.create(doacao=d1, produto=c_feijao,   quantidade=15, unidade='kg',      data_validade=date(2026, 12, 10))
        ItemDoacao.objects.create(doacao=d1, produto=c_oleo,     quantidade=10, unidade='unidade', data_validade=date(2026, 10, 1))

        d2 = Doacao.objects.create(
            doador='João Anônimo', data=date(2026, 5, 20),
            descricao='Doação de roupas em boas condições.',
            paroquia=parq_sj, registrado_por=vol_sj,
        )
        ItemDoacao.objects.create(doacao=d2, produto=c_camisa, quantidade=7, unidade='unidade')
        ItemDoacao.objects.create(doacao=d2, produto=c_blusa,  quantidade=3, unidade='unidade')

        d3 = Doacao.objects.create(
            doador='Paróquia São Francisco', data=date(2026, 6, 1),
            descricao='Doação solidária entre paróquias para abastecimento do estoque.',
            paroquia=parq_sj, registrado_por=coord_sj,
        )
        ItemDoacao.objects.create(doacao=d3, produto=c_macarrao, quantidade=30, unidade='pacote', data_validade=date(2026, 11, 20))
        ItemDoacao.objects.create(doacao=d3, produto=c_acucar,   quantidade=20, unidade='kg',     data_validade=date(2027, 3, 1))
        ItemDoacao.objects.create(doacao=d3, produto=c_leite,    quantidade=15, unidade='lata',   data_validade=date(2026, 6, 28))
        self.stdout.write('  ✓ Doações (3) com 8 itens')

        # ── 7. Atendimentos ────────────────────────────────────────────────────
        Atendimento.objects.create(
            familia=f_maria, tipo='assistencia_social', data=date(2026, 6, 5),
            descricao='Orientação sobre benefícios sociais e encaminhamento para o CRAS.',
            paroquia=parq_sj, registrado_por=coord_sj,
        )

        at_roupas = Atendimento.objects.create(
            familia=f_maria, tipo='doacao_roupas', data=date(2026, 6, 10),
            descricao='Doação de roupas masculinas para a família.',
            paroquia=parq_sj, registrado_por=vol_sj,
        )
        ItemAtendimento.objects.create(
            atendimento=at_roupas, item_estoque=e_camisa,
            item_nome='Camisa', item_unidade='unidade', quantidade=2,
        )

        Atendimento.objects.create(
            familia=f_joao, tipo='visita_domiciliar', data=date(2026, 5, 15),
            descricao='Levantamento das condições habitacionais da família.',
            paroquia=parq_sj, registrado_por=coord_sj,
        )
        Atendimento.objects.create(
            familia=f_ana, tipo='doacao_cesta_basica', data=date(2026, 6, 12),
            descricao='Entrega de cesta básica. Família em situação de extrema vulnerabilidade.',
            paroquia=parq_sj, registrado_por=coord_sj,
        )
        Atendimento.objects.create(
            familia=f_carlos, tipo='encaminhamento', data=date(2026, 6, 15),
            descricao='Encaminhamento para apoio a refugiados na paróquia Nossa Senhora Aparecida.',
            paroquia=parq_sj, paroquia_destino=parq_nsa, registrado_por=coord_sj,
        )
        Atendimento.objects.create(
            familia=f_fernanda, tipo='assistencia_social', data=date(2026, 4, 20),
            descricao='Análise de elegibilidade para BPC (Benefício de Prestação Continuada).',
            paroquia=parq_sj, registrado_por=coord_sj,
        )
        Atendimento.objects.create(
            familia=f_fernanda, tipo='outro', tipo_outro='Orientação jurídica',
            data=date(2026, 6, 18),
            descricao='Orientação sobre regularização de imóvel para fins de acessibilidade.',
            paroquia=parq_sj, registrado_por=vol_sj,
        )
        self.stdout.write('  ✓ Atendimentos (7) — todos os 6 tipos cobertos')

        # ── 8. Cestas ──────────────────────────────────────────────────────────
        # CestaPronta montagem — itens do estoque já descontados nas qtds finais acima
        cesta1 = CestaPronta.objects.create(
            paroquia=parq_sj, quantidade=10, origem='montagem', data=date(2026, 6, 3),
            observacao='Montagem para distribuição da campanha do inverno.',
            registrado_por=coord_sj,
        )
        for est_item, qtd in [(e_arroz, 10), (e_feijao, 10), (e_oleo, 10), (e_macarrao, 10), (e_acucar, 10)]:
            ItemMontagem.objects.create(
                cesta_pronta=cesta1, item_estoque=est_item,
                item_nome=est_item.nome, quantidade_total=qtd,
            )

        CestaPronta.objects.create(
            paroquia=parq_sj, quantidade=5, origem='doacao', data=date(2026, 6, 8),
            observacao='Cestas prontas doadas pela campanha solidária do Lions Club.',
            registrado_por=coord_sj,
        )

        for f, qtd, dt in [
            (f_maria,   1, date(2026, 6, 5)),
            (f_ana,     1, date(2026, 6, 12)),
            (f_fernanda, 2, date(2026, 6, 18)),
        ]:
            EntregaCesta.objects.create(
                familia=f, paroquia=parq_sj, quantidade=qtd,
                data=dt, registrado_por=coord_sj,
            )
        self.stdout.write('  ✓ Cestas (2 entradas, 3 entregas)')

        # ── 9. Bazar ───────────────────────────────────────────────────────────
        cb_cam_m = CatalogoBazar.objects.create(nome='Camiseta',   genero='masculino')
        cb_cam_f = CatalogoBazar.objects.create(nome='Camiseta',   genero='feminino')
        cb_cal_m = CatalogoBazar.objects.create(nome='Calça Jeans',genero='masculino')
        cb_ves_f = CatalogoBazar.objects.create(nome='Vestido',    genero='feminino')
        cb_jaq   = CatalogoBazar.objects.create(nome='Jaqueta',    genero='unissex')
        cb_conj  = CatalogoBazar.objects.create(nome='Conjunto',   genero='infantil')

        empresa1 = EmpresaParceira.objects.create(
            nome='Renova Modas Ltda', cnpj='12.345.678/0001-90',
            contato_nome='Adriana Ferreira', contato_telefone='(54) 99100-2020',
            contato_email='adriana@renovamodas.com.br',
        )
        EmpresaParceira.objects.create(
            nome='Mercado São Bento', cnpj='98.765.432/0001-11',
            contato_nome='Pedro Bento', contato_telefone='(54) 3400-1111',
        )

        # Estoque bazar — quantidades FINAIS (após as 5 vendas abaixo)
        eb_cam_m = ItemEstoqueBazar.objects.create(catalogo=cb_cam_m, tamanho='m',     estado='bom',     quantidade=12, preco_sugerido=5.00,  registrado_por=coord_bazar)
        eb_cam_f = ItemEstoqueBazar.objects.create(catalogo=cb_cam_f, tamanho='p',     estado='bom',     quantidade=10, preco_sugerido=5.00,  registrado_por=coord_bazar)
        eb_cal_m = ItemEstoqueBazar.objects.create(catalogo=cb_cal_m, tamanho='g',     estado='regular', quantidade=7,  preco_sugerido=10.00, registrado_por=coord_bazar)
        eb_ves_f = ItemEstoqueBazar.objects.create(catalogo=cb_ves_f, tamanho='m',     estado='novo',    quantidade=4,  preco_sugerido=12.00, registrado_por=coord_bazar)
        ItemEstoqueBazar.objects.create(            catalogo=cb_jaq,  tamanho='gg',    estado='bom',     quantidade=4,  preco_sugerido=15.00, registrado_por=coord_bazar)
        eb_conj  = ItemEstoqueBazar.objects.create(catalogo=cb_conj,  tamanho='unico', estado='bom',     quantidade=6,  preco_sugerido=8.00,  registrado_por=coord_bazar)

        # Entrada com itens (quantidades originais antes das vendas)
        ent1 = EntradaBazar.objects.create(
            tipo_entrada='doacao_item', tipo_doador='empresa', empresa=empresa1,
            data=date(2026, 5, 15),
            observacao='Doação de peças da coleção anterior da loja.',
            registrado_por=coord_bazar,
        )
        for cat, tam, est, qtd, preco in [
            (cb_cam_m, 'm',     'bom',     15, 5.00),
            (cb_cam_f, 'p',     'bom',     12, 5.00),
            (cb_cal_m, 'g',     'regular',  8, 10.00),
            (cb_ves_f, 'm',     'novo',     6, 12.00),
            (cb_jaq,   'gg',    'bom',      4, 15.00),
            (cb_conj,  'unico', 'bom',     10, 8.00),
        ]:
            ItemEntradaBazar.objects.create(
                entrada=ent1, catalogo=cat, tamanho=tam,
                estado=est, quantidade=qtd, preco_sugerido=preco,
            )

        EntradaBazar.objects.create(
            tipo_entrada='doacao_financeira', tipo_doador='pessoa_fisica',
            doador_nome='Márcia Rodrigues', doador_contato='(54) 99800-7766',
            valor=500.00, data=date(2026, 6, 1),
            observacao='Doação espontânea para custear despesas do bazar.',
            registrado_por=coord_bazar,
        )

        # Vendas — gera numero_operacao igual à view: "{ano}-{pk:05d}"
        for item, qtd, preco, dt in [
            (eb_cam_m, 3, 5.00,  date(2026, 6, 10)),
            (eb_cam_f, 2, 5.00,  date(2026, 6, 10)),
            (eb_cal_m, 1, 10.00, date(2026, 6, 12)),
            (eb_ves_f, 2, 12.00, date(2026, 6, 15)),
            (eb_conj,  4, 8.00,  date(2026, 6, 20)),
        ]:
            v = Venda(item=item, quantidade=qtd, preco_unitario=preco,
                      data=dt, paroquia=parq_sj, registrado_por=coord_bazar)
            v.save()
            v.numero_operacao = f'2026-{v.pk:05d}'
            v.save(update_fields=['numero_operacao'])
        self.stdout.write('  ✓ Bazar (6 catálogos, 2 empresas, 2 entradas, 5 vendas — R$ 91,00)')

        # ── 10. Brechó ─────────────────────────────────────────────────────────
        evento = BrechoEvento.objects.create(
            nome='Brechó de Outono', paroquia=parq_sj, data=date(2026, 6, 21),
            descricao='Evento de brechó com peças do estoque. Renda revertida para a Cáritas.',
            status='em_andamento', criado_por=coord_sj,
        )
        # Estoque de roupas já descontado nas qtds finais acima (5 camisas, 3 calças usadas)
        for est_item, qtd, preco in [
            (e_camisa, 2, 4.00),
            (e_calca,  1, 6.00),
            (e_camisa, 3, 4.00),
            (e_calca,  2, 6.00),
        ]:
            VendaBrecho.objects.create(
                evento=evento, item_estoque=est_item, item_nome=est_item.nome,
                quantidade=qtd, preco_unitario=preco, registrado_por=coord_sj,
            )
        self.stdout.write('  ✓ Brechó (1 evento em andamento, 4 vendas — R$ 38,00)')

        # ── 11. Financeiro ─────────────────────────────────────────────────────
        for origem, parq, tipo, valor, dt, desc in [
            ('paroquia', parq_sj,  'entrada_doacao',         1200.00, date(2026, 5, 5),  'Doação em dinheiro de fiéis após missa dominical.'),
            ('paroquia', parq_sj,  'entrada_vendas',          340.00, date(2026, 6, 10), 'Receita de vendas do bazar — mai/jun 2026.'),
            ('paroquia', parq_sj,  'saida_insumos',           580.00, date(2026, 5, 20), 'Compra de insumos para reposição do estoque de alimentos.'),
            ('diocese',  None,     'saida_projeto',           200.00, date(2026, 6, 1),  'Materiais para projeto de apoio a refugiados.'),
            ('paroquia', parq_nsa, 'entrada_doacao',          800.00, date(2026, 5, 28), 'Arrecadação na Festa de Nossa Senhora Aparecida.'),
            ('diocese',  None,     'saida_doacao_terceiros',  150.00, date(2026, 6, 15), 'Doação para o projeto TETO de habitação social.'),
            ('paroquia', parq_sj,  'entrada_vendas',           38.00, date(2026, 6, 21), 'Receita do Brechó de Outono.'),
        ]:
            MovimentacaoFinanceira.objects.create(
                origem=origem, paroquia=parq, tipo=tipo,
                valor=valor, data=dt, descricao=desc,
                registrado_por=coord_sj,
            )
        self.stdout.write('  ✓ Financeiro (7 movimentações)')

        # ── Resumo ─────────────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS('\n✅ Seed concluído com sucesso!\n'))
        self.stdout.write('   Logins disponíveis (senha: senha123):')
        self.stdout.write('   admin        — Administrador (senha = DJANGO_SUPERUSER_PASSWORD do Render)')
        self.stdout.write('   coord_sj     — Coordenador São José')
        self.stdout.write('   vol_sj       — Voluntário São José')
        self.stdout.write('   coord_nsa    — Coordenador N. Sra. Aparecida')
        self.stdout.write('   coord_bazar  — Coordenador do Bazar (sem paróquia)\n')
