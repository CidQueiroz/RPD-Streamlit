import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Estoque, Venda, Atividade, DiarioBordo, RPD, LogPODDiario

class Command(BaseCommand):
    help = 'Migrates data from the old rpd_streamlit SQL dump file.'

    def add_arguments(self, parser):
        parser.add_argument('sql_dump_file', type=str, help='The path to the SQL dump file.')

    def handle(self, *args, **options):
        sql_file_path = options['sql_dump_file']
        self.stdout.write(self.style.SUCCESS(f'Starting data migration from {sql_file_path}...'))

        with open(sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # --- 1. Migrate Users ---
        self.stdout.write('Migrating users...')
        user_inserts_raw = re.search(r"INSERT INTO `usuarios` VALUES (.*?);", content, re.DOTALL)
        old_user_map = {}
        User = get_user_model()

        if user_inserts_raw:
            user_value_sets = re.split(r'\),\s*\(', user_inserts_raw.group(1).strip('()'))
            
            for user_data_str in user_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*(\d+),\s*(\d+),\s*(\d+)", user_data_str)
                    if match:
                        old_id = int(match.group(1))
                        username = match.group(2)
                        password = 'password123'
                        email = f"{username}@example.com" 

                        if not User.objects.filter(email=email).exists():
                            new_user = User.objects.create_user(email=email, password=password, is_active=True)
                            old_user_map[old_id] = new_user.id
                            self.stdout.write(f'  Created user: {email}')
                        else:
                            new_user = User.objects.get(email=email)
                            if not new_user.is_active:
                                new_user.is_active = True
                                new_user.save()
                            old_user_map[old_id] = new_user.id
                            self.stdout.write(f'  User already exists: {email}')
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse user data with regex: {user_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing user data "{user_data_str}": {e}'))


        # --- 2. Migrate Estoque ---
        self.stdout.write('Migrating estoque...')
        estoque_inserts_raw = re.search(r"INSERT INTO `estoque` \(`id_item`, `item`, `variacao`, `quantidade`, `preco`, `empresa_fk`\) VALUES (.*?);", content, re.DOTALL)
        old_estoque_map = {}

        if estoque_inserts_raw:
            estoque_value_sets = re.split(r'\),\s*\(', estoque_inserts_raw.group(1).strip('()'))

            for estoque_data_str in estoque_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'((?:[^']|\\')*)',\s*(?:'((?:[^']|\\')*)'|NULL),\s*(\d+),\s*(\d+\.\d+),\s*(\d+)", estoque_data_str)
                    if match:
                        old_id = int(match.group(1))
                        item_name = match.group(2)
                        variacao = match.group(3) if match.group(3) else ''
                        quantidade = int(match.group(4))
                        preco = float(match.group(5))
                        
                        usuario_id = old_user_map.get(1) 

                        if usuario_id:
                            estoque_item, created = Estoque.objects.get_or_create(
                                usuario_id=usuario_id,
                                item=item_name,
                                variacao=variacao,
                                defaults={'quantidade': quantidade, 'preco': preco}
                            )
                            old_estoque_map[old_id] = estoque_item.id
                            if created:
                                self.stdout.write(f'  Created estoque: {item_name} ({variacao})')
                            else:
                                self.stdout.write(f'  Estoque already exists: {item_name} ({variacao})')
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse estoque data with regex: {estoque_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing estoque data "{estoque_data_str}": {e}'))

        # --- 3. Migrate Vendas ---
        self.stdout.write('Migrating vendas...')
        venda_inserts_raw = re.search(r"INSERT INTO `vendas` \(`id_venda`, `data_hora`, `quantidade`, `preco_unitario`, `vendedor_fk`, `estoque_fk`, `empresa_fk`\) VALUES \((.*?)\);", content, re.DOTALL)
        
        if venda_inserts_raw:
            venda_value_sets = re.split(r'\),\s*\(', venda_inserts_raw.group(1).strip('()'))

            for venda_data_str in venda_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'([^']*)',\s*(\d+),\s*(\d+\.\d+),\s*(\d+),\s*(\d+),\s*(\d+)", venda_data_str)
                    if match:
                        quantidade = int(match.group(3))
                        old_vendedor_id = int(match.group(5))
                        old_estoque_id = int(match.group(6))

                        new_usuario_id = old_user_map.get(old_vendedor_id)
                        new_estoque_id = old_estoque_map.get(old_estoque_id)

                        if new_usuario_id and new_estoque_id:
                            Venda.objects.get_or_create(
                                usuario_id=new_usuario_id,
                                estoque_item_id=new_estoque_id,
                                quantidade=quantidade,
                            )
                            self.stdout.write(f'  Created venda for user {new_usuario_id} and item {new_estoque_id}')
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse venda data with regex: {venda_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing venda data "{venda_data_str}": {e}'))

        # --- 4. Migrate Atividades ---
        self.stdout.write('Migrating atividades...')
        atividade_inserts_raw = re.search(r"INSERT INTO `atividades` VALUES (.*?);", content, re.DOTALL)
        old_atividade_map = {}
        
        if atividade_inserts_raw:
            atividade_value_sets = re.split(r'\),\s*\(', atividade_inserts_raw.group(1).strip('()'))

            for atividade_data_str in atividade_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'((?:[^']|\\')*)',\s*'((?:[^']|\\')*)',\s*(\d+),\s*(\d+)", atividade_data_str)
                    if match:
                        old_id = int(match.group(1))
                        nome_atividade = match.group(2)
                        periodo = match.group(3)
                        ativa = bool(int(match.group(4)))
                        old_usuario_id = int(match.group(5))

                        new_usuario_id = old_user_map.get(old_usuario_id)

                        if new_usuario_id:
                            atividade, created = Atividade.objects.get_or_create(
                                usuario_id=new_usuario_id,
                                nome_atividade=nome_atividade,
                                defaults={'periodo': periodo, 'ativa': ativa}
                            )
                            old_atividade_map[old_id] = atividade.id
                            if created:
                                self.stdout.write(f'  Created atividade: {nome_atividade}')
                            else:
                                self.stdout.write(f'  Atividade already exists: {nome_atividade}')
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse atividade data with regex: {atividade_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing atividade data "{atividade_data_str}": {e}'))

        # --- 5. Migrate DiarioBordo ---
        self.stdout.write('Migrating diario_bordo...')
        diario_bordo_inserts_raw = re.search(r"INSERT INTO `diario_bordo` VALUES (.*?);", content, re.DOTALL)

        if diario_bordo_inserts_raw:
            diario_bordo_value_sets = re.split(r'\),\s*\(', diario_bordo_inserts_raw.group(1).strip('()'))

            for diario_bordo_data_str in diario_bordo_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'([^']*)',\s*(\d+),\s*(\d+)", diario_bordo_data_str)
                    if match:
                        data = match.group(2)
                        old_usuario_id = int(match.group(3))
                        old_atividade_id = int(match.group(4))

                        new_usuario_id = old_user_map.get(old_usuario_id)
                        new_atividade_id = old_atividade_map.get(old_atividade_id)

                        if new_usuario_id and new_atividade_id:
                            DiarioBordo.objects.get_or_create(
                                usuario_id=new_usuario_id,
                                atividade_id=new_atividade_id,
                                data=data,
                            )
                            self.stdout.write(f'  Created diario_bordo entry for user {new_usuario_id} and activity {new_atividade_id}')
                        else:
                            self.stdout.write(self.style.WARNING(f'  Could not find user or activity for diario_bordo entry: {diario_bordo_data_str}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse diario_bordo data with regex: {diario_bordo_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing diario_bordo data "{diario_bordo_data_str}": {e}'))

        # --- 6. Migrate RPD ---
        self.stdout.write('Migrating RPD...')
        rpd_inserts_raw = re.search(r"INSERT INTO `respostas` VALUES (.*?);", content, re.DOTALL)

        if rpd_inserts_raw:
            rpd_value_sets = re.split(r'\),\s*\(', rpd_inserts_raw.group(1).strip('()'))

            for rpd_data_str in rpd_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'([^']*)',\s*'((?:[^']|\\')*)',\s*'((?:[^']|\\')*)',\s*'((?:[^']|\\')*)',\s*'((?:[^']|\\')*)',\s*'((?:[^']|\\')*)',\s*(\d+)", rpd_data_str)
                    if match:
                        data = match.group(2)
                        situacao = match.group(3)
                        pensamento_automatico = match.group(4)
                        emocao = match.group(5)
                        resposta_adaptativa = match.group(6)
                        resultado = match.group(7)
                        old_usuario_id = int(match.group(8))

                        new_usuario_id = old_user_map.get(old_usuario_id)

                        if new_usuario_id:
                            RPD.objects.get_or_create(
                                usuario_id=new_usuario_id,
                                data=data,
                                defaults={
                                    'situacao': situacao,
                                    'pensamento_automatico': pensamento_automatico,
                                    'emocao': emocao,
                                    'resposta_adaptativa': resposta_adaptativa,
                                    'resultado': resultado,
                                }
                            )
                            self.stdout.write(f'  Created RPD entry for user {new_usuario_id}')
                        else:
                            self.stdout.write(self.style.WARNING(f'  Could not find user for RPD entry: {rpd_data_str}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse RPD data with regex: {rpd_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing RPD data "{rpd_data_str}": {e}'))

        # --- 7. Migrate LogPODDiario ---
        self.stdout.write('Migrating LogPODDiario...')
        log_pod_diario_inserts_raw = re.search(r"INSERT INTO `log_pod_diario` VALUES (.*?);", content, re.DOTALL)

        if log_pod_diario_inserts_raw:
            log_pod_diario_value_sets = re.split(r'\),\s*\(', log_pod_diario_inserts_raw.group(1).strip('()'))

            for log_pod_diario_data_str in log_pod_diario_value_sets:
                try:
                    match = re.match(r"(\d+),\s*'([^']*)',\s*(\d+),\s*(\d+),\s*(\d+)", log_pod_diario_data_str)
                    if match:
                        data = match.group(2)
                        status = bool(int(match.group(3)))
                        old_usuario_id = int(match.group(4))
                        old_atividade_id = int(match.group(5))

                        new_usuario_id = old_user_map.get(old_usuario_id)
                        new_atividade_id = old_atividade_map.get(old_atividade_id)

                        if new_usuario_id and new_atividade_id:
                            LogPODDiario.objects.get_or_create(
                                usuario_id=new_usuario_id,
                                atividade_id=new_atividade_id,
                                data=data,
                                defaults={'status': status}
                            )
                            self.stdout.write(f'  Created LogPODDiario entry for user {new_usuario_id} and activity {new_atividade_id}')
                        else:
                            self.stdout.write(self.style.WARNING(f'  Could not find user or activity for LogPODDiario entry: {log_pod_diario_data_str}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  Could not parse LogPODDiario data with regex: {log_pod_diario_data_str}'))
                except (ValueError) as e:
                    self.stdout.write(self.style.ERROR(f'  Error parsing LogPODDiario data "{log_pod_diario_data_str}": {e}'))

        self.stdout.write(self.style.SUCCESS('Data migration completed successfully!'))
