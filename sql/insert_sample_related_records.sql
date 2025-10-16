-- Associa os técnicos e contatos às empresas.
DECLARE
  V_ID_TECNICO_CARLOS   NUMBER;
  V_ID_TECNICO_MARCOS   NUMBER;
  V_ID_CONTATO_ANA      NUMBER;
  V_ID_EMPRESA_LOGTRANS NUMBER;
  V_ID_EMPRESA_SERRA    NUMBER;
  V_ID_EMPRESA_VV       NUMBER;
BEGIN
  -- Busca os IDs dos contatos e transforma-os em IDs de técnicos
  SELECT id_tecnico INTO V_ID_TECNICO_CARLOS FROM TECNICOS WHERE id_contato = (SELECT id_contato FROM CONTATOS WHERE nome_contato = 'Carlos Andrade');
  SELECT id_tecnico INTO V_ID_TECNICO_MARCOS FROM TECNICOS WHERE id_contato = (SELECT id_contato FROM CONTATOS WHERE nome_contato = 'Marcos Oliveira');

  -- Busca o ID do contato 'Ana Beatriz', que não é um técnico
  SELECT id_contato INTO V_ID_CONTATO_ANA FROM CONTATOS WHERE nome_contato = 'Ana Beatriz Costa';

  -- Busca os IDs das empresas
  SELECT id_empresa INTO V_ID_EMPRESA_LOGTRANS FROM EMPRESAS WHERE nome_fantasia = 'LogTrans Cargas Rápidas';
  SELECT id_empresa INTO V_ID_EMPRESA_SERRA FROM EMPRESAS WHERE nome_fantasia = 'Serra Solutions Tech';
  SELECT id_empresa INTO V_ID_EMPRESA_VV FROM EMPRESAS WHERE nome_fantasia = 'Vila Velha Transportes';

  -- Associa o técnico Carlos a duas empresas (exemplo de muitos-para-muitos)
  INSERT INTO TECNICOS_EMPRESAS (id_tecnico, id_empresa) VALUES (V_ID_TECNICO_CARLOS, V_ID_EMPRESA_LOGTRANS);
  INSERT INTO TECNICOS_EMPRESAS (id_tecnico, id_empresa) VALUES (V_ID_TECNICO_CARLOS, V_ID_EMPRESA_SERRA);

  -- Associa o técnico Marcos a uma empresa
  INSERT INTO TECNICOS_EMPRESAS (id_tecnico, id_empresa) VALUES (V_ID_TECNICO_MARCOS, V_ID_EMPRESA_VV);

  -- Associa a Ana Beatriz (que é apenas um contato) a uma empresa
  INSERT INTO EMPRESA_CONTATOS (id_empresa, id_contato) VALUES (V_ID_EMPRESA_LOGTRANS, V_ID_CONTATO_ANA);
END;

-- Bloco 2: Simula um ciclo completo de manutenção para o veículo 'RDM4E56'.
DECLARE
  V_ID_VEICULO      NUMBER;
  V_ID_TECNICO      NUMBER;
  V_ID_VISITA       NUMBER;
  V_ID_DEFEITO      NUMBER;
  V_ID_MANUTENCAO   NUMBER;
  V_ID_CAT_DEFEITO  NUMBER;
  V_ID_CAT_ACAO     NUMBER;
  V_ID_CAT_EVENTO   NUMBER;
  V_ID_LOT          NUMBER;
BEGIN
  -- Busca os IDs dos registros de referência
  SELECT id_veiculo INTO V_ID_VEICULO FROM VEICULOS WHERE placa = 'RDM4E56';
  SELECT id_tecnico INTO V_ID_TECNICO FROM TECNICOS WHERE id_contato = (SELECT id_contato FROM CONTATOS WHERE nome_contato = 'Carlos Andrade');
  -- CORREÇÃO: Usando um código de defeito que existe
  SELECT id_catalogo_defeito INTO V_ID_CAT_DEFEITO FROM CATALOGO_DEFEITOS WHERE codigo_defeito = 'SEM_COMUNICACAO';
  -- CORREÇÃO: Usando um código de ação que existe
  SELECT id_catalogo_acao INTO V_ID_CAT_ACAO FROM CATALOGO_ACOES WHERE codigo_acao = 'MANUTENCAO_SIMPLES';
  SELECT id_lot INTO V_ID_LOT FROM LOTS WHERE codigo_lot = 'LOT1001';

  -- 1. Cria a visita e guarda o ID gerado
  INSERT INTO VISITAS_TECNICAS (id_visita, id_tecnico, data_visita)
  VALUES (SEQ_VISITAS_TECNICAS.NEXTVAL, V_ID_TECNICO, SYSDATE)
  RETURNING id_visita INTO V_ID_VISITA;

  -- 2. Cria o defeito e guarda o ID gerado
  INSERT INTO DEFEITOS (id_defeito, id_catalogo_defeito, id_veiculo, data_reporte, status_defeito, obs_defeitos)
  VALUES (SEQ_DEFEITOS.NEXTVAL, V_ID_CAT_DEFEITO, V_ID_VEICULO, SYSDATE, 'ABERTO', 'Veículo reportado sem comunicação desde ontem.')
  RETURNING id_defeito INTO V_ID_DEFEITO;

  -- 3. Cria a manutenção, usando os IDs guardados
  INSERT INTO MANUTENCOES (id_manutencao, id_visita, id_catalogo_acao, id_defeito, obs_servico)
  VALUES (SEQ_MANUTENCOES.NEXTVAL, V_ID_VISITA, V_ID_CAT_ACAO, V_ID_DEFEITO, 'Realizado reinício remoto do dispositivo e verificação de cabos.')
  RETURNING id_manutencao INTO V_ID_MANUTENCAO;

  -- 4. Atualiza o status do defeito para 'FECHADO'
  UPDATE DEFEITOS SET status_defeito = 'FECHADO' WHERE id_defeito = V_ID_DEFEITO;

  -- 5. Registra o evento no LOG_LOT
  SELECT id_catalogo_eventos INTO V_ID_CAT_EVENTO FROM CATALOGO_EVENTOS WHERE codigo_evento = 'MANUTENCAO_SEDE'; -- Pode ser 'MANUTENCAO_CAMPO' se existir
  INSERT INTO LOG_LOT (id_log, id_lot, id_veiculo, id_manutencao, id_catalogo_eventos, data_evento, responsavel_evento, obs_evento)
  VALUES (SEQ_LOG_LOT.NEXTVAL, V_ID_LOT, V_ID_VEICULO, V_ID_MANUTENCAO, V_ID_CAT_EVENTO, SYSDATE, 'Carlos Andrade', 'Manutenção corretiva realizada em campo.');
END;

COMMIT;