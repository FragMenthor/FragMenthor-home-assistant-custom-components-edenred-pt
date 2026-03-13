<p align="left">
  <img src="https://raw.githubusercontent.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/main/custom_components/edenred_pt/logo.png" alt="Edenred Portugal" width="500">
</p>

# Edenred PT — Integração para Home Assistant

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![License](https://img.shields.io/github/license/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt)
![Release](https://img.shields.io/github/v/release/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt)
Integração para obter saldos e movimentos dos cartões **Edenred Portugal** diretamente no Home Assistant.

## ✨ Funcionalidades

- Login com autenticação por **API NÃO OFICIAL** da Edenred
- Token temporário armazenado em memória
- Suporte para **vários cartões**
- Atualização configurável (e reconfigurável): **15 min a 12 horas**
- Sensor de saldo por cartão, com dados do cartão em atributos
- Sensor de último movimento (com atributos completos e histórico de movimentos)
- Compatível com **HACS (Custom Repo)**
- Serviço `edenred_pt.force_update` para forçar atualização de dados

## 📦 Instalação via HACS

1. Em **HACS → Custom repositories**, adicionar `https://github.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt`
2. Tipo: **Integration**
3. Instalar e reiniciar o Home Assistant

## 🔧 Configuração

1. **Configurações → Dispositivos e Serviços → Adicionar Integração**
2. Procurar **Edenred Portugal**
3. Introduzir Email, Password e Intervalo de atualização (15–720 min)

## 🧩 Sensores criados

Para cada cartão são criados dois sensores:

- `sensor.edenred_<id>_saldo`
- `sensor.edenred_<id>_ultimo_movimento`

Atributos do último movimento:
- `transaction_date`, `date`, `time`, `date_time`, `description`, `category`, `cat` _(abreviatura)_, `type` _(símbolo)_, `t` _(ícone colorido)_, `balance_after` e `movements` _(lista de movimentos, com (_`amount`_)_.

## 📜 Licença

MIT License
