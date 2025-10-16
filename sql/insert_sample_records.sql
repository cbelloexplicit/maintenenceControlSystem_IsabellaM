-- Inserir dados no catálogo de eventos
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'INSTALACAO');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'DESINSTALACAO');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'TRANSFERENCIA_UNIDADE');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'ENVIO_PARA_SEDE');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'ENVIO_PARA_TRANSPORTADORA');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'MANUTENCAO_SEDE');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'AGUARDANDO_ENVIO_PARA_SEDE');
INSERT INTO CATALOGO_EVENTOS (id_catalogo_eventos, codigo_evento) VALUES (SEQ_CATALOGO_EVENTOS.NEXTVAL, 'INOPERANTE');

-- Insere dados no catálogo de acoes
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'INSTALACAO', 'Instalação de novo LOT em veículo');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'DESINSTALACAO', 'Desinstalação do módulo em veículo');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'TROCA', 'Troca de LOT em veículo');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'MANUTENCAO_SIMPLES', 'Manutenção e ajuste');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'CALIBRACAO', 'Calibração de câmeras e reposicionamento');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'TRANSFERENCIA', 'Transferência de equipamento de veículo A <-> B');
INSERT INTO CATALOGO_ACOES (id_catalogo_acao, codigo_acao, descricao_acao) VALUES (SEQ_CATALOGO_ACOES.NEXTVAL, 'OUTROS', 'Especificar em comentários');

-- Insere dados no catálogo de defeitos
INSERT INTO CATALOGO_DEFEITOS (id_catalogo_defeito, codigo_defeito, descricao_defeito) VALUES (SEQ_CATALOGO_DEFEITOS.NEXTVAL, 'SEM_COMUNICACAO', 'Troca prioritária');
INSERT INTO CATALOGO_DEFEITOS (id_catalogo_defeito, codigo_defeito, descricao_defeito) VALUES (SEQ_CATALOGO_DEFEITOS.NEXTVAL, 'FALHA_CAMERA', 'Mau contato no cabo flat externo');
INSERT INTO CATALOGO_DEFEITOS (id_catalogo_defeito, codigo_defeito) VALUES (SEQ_CATALOGO_DEFEITOS.NEXTVAL, 'FALHA_IR');
INSERT INTO CATALOGO_DEFEITOS (id_catalogo_defeito, codigo_defeito) VALUES (SEQ_CATALOGO_DEFEITOS.NEXTVAL, 'INTERNA_SEM_COMUNICAR');

-- Inserir dados de Empresas
INSERT INTO EMPRESAS (id_empresa, nome_fantasia, endereco) VALUES (SEQ_EMPRESAS.NEXTVAL, 'LogTrans Cargas Rápidas', 'Rodovia do Contorno, 100, Cariacica/ES');
INSERT INTO EMPRESAS (id_empresa, nome_fantasia, endereco) VALUES (SEQ_EMPRESAS.NEXTVAL, 'Serra Solutions Tech', 'Av. Civit, 1295, Serra/ES');
INSERT INTO EMPRESAS (id_empresa, nome_fantasia, endereco) VALUES (SEQ_EMPRESAS.NEXTVAL, 'Vila Velha Transportes', 'Av. da Praia, 500, Vila Velha/ES');

-- Inserir dados de contatos
INSERT INTO CONTATOS (id_contato, nome_contato, email_contato, telefone) VALUES (SEQ_CONTATOS.NEXTVAL, 'Carlos Andrade', 'carlos.a@email.com', '27999991111');
INSERT INTO CONTATOS (id_contato, nome_contato, email_contato) VALUES (SEQ_CONTATOS.NEXTVAL, 'Ana Beatriz Costa', 'ana.b@email.com');
INSERT INTO CONTATOS (id_contato, nome_contato, telefone) VALUES (SEQ_CONTATOS.NEXTVAL, 'Marcos Oliveira', '27999992222');

-- Inserir um dispositivo (Lot)
INSERT INTO LOTS (id_lot, codigo_lot, obs_lot) VALUES (SEQ_LOTS.NEXTVAL, 'LOT1001', 'Rastreador GPS Modelo A');
INSERT INTO LOTS (id_lot, codigo_lot, obs_lot) VALUES (SEQ_LOTS.NEXTVAL, 'LOT2502', 'Rastreador GPS Modelo A');
INSERT INTO LOTS (id_lot, codigo_lot, obs_lot) VALUES (SEQ_LOTS.NEXTVAL, 'LOT1233', 'Rastreador GPS Modelo A');
INSERT INTO LOTS (id_lot, codigo_lot) VALUES (SEQ_LOTS.NEXTVAL, 'LOT1901');

-- Inserir usuario (com senha criptografada e ponto e vírgula)
INSERT INTO USUARIOS (id_usuario, nome_completo, email_usuario, senha) VALUES (SEQ_USUARIOS.NEXTVAL, 'Administrador Padrão','admin@sistema.com','senha123');
INSERT INTO USUARIOS (id_usuario, nome_completo, email_usuario, senha) VALUES (SEQ_USUARIOS.NEXTVAL, 'Isabella M.','isabella.m@sistema.com','senha123');
INSERT INTO USUARIOS (id_usuario, nome_completo, email_usuario, senha) VALUES (SEQ_USUARIOS.NEXTVAL, 'Usuário de Teste','teste@sistema.com','senha123');

-- ligar contato a tecnico
INSERT INTO TECNICOS (id_tecnico, local, id_contato) VALUES (SEQ_TECNICOS.NEXTVAL, 'Grande Vitória', 1);
INSERT INTO TECNICOS (id_tecnico, local, id_contato) VALUES (SEQ_TECNICOS.NEXTVAL, 'Região Serrana', 3);

-- inserir veiculo (Assumindo que os IDs das empresas serão 1, 2, 3)
INSERT INTO VEICULOS (id_veiculo, placa, frota, id_empresa) VALUES (SEQ_VEICULOS.NEXTVAL, 'RDM4E56', '0806', 1);
INSERT INTO VEICULOS (id_veiculo, placa, frota, id_empresa) VALUES (SEQ_VEICULOS.NEXTVAL, 'ABC1D23', '10000', 2);
INSERT INTO VEICULOS (id_veiculo, placa, frota, id_empresa) VALUES (SEQ_VEICULOS.NEXTVAL, 'QWE9F87', '250901', 1);

COMMIT;