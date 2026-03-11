
<p align="center">
  <img src="https://raw.githubusercontent.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/refs/heads/main/custom_components/edenred_pt/icon.png" alt="Edenred Portugal" width="128">
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/FragMenthor/FragMenthor-home-assistant-custom-components-edenred-pt/main/custom_components/edenred_pt/logo.png" alt="Edenred Portugal" width="500">
</p>

# Edenred PT — Integração para Home Assistant

![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![License](https://img.shields.io/github/license/FragMenthor/home-assistant-custom-components-edenred-pt)
![Release](https://img.shields.io/github/v/release/FragMenthor/home-assistant-custom-components-edenred-pt)

Integração para obter saldos e movimentos dos cartões **Edenred Portugal** diretamente no Home Assistant.

## ✨ Funcionalidades

- Login com autenticação por API NÃO OFICIAL da Edenred
- Token temporário armazenado em memória
- Suporte para **vários cartões**
- Atualização configurável: **15 min a 12 horas**
- Sensor de saldo por cartão
- Sensor de último movimento (com atributos completos)
- Compatível com **HACS (Custom Repo)**

## 📦 Instalação via HACS

1. Em **HACS → Custom repositories**, adicionar `https://github.com/FragMenthor/home-assistant-custom-components-edenred-pt`
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
- `date`, `description`, `category`, `balance_after`

## 📜 Licença

MIT License
